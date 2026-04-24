"""
Evaluation pipeline: tests the RAG agent against a set of predefined questions
and compares chunking strategies.
"""

import json
import time
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from data_loader import load_all_documents
from rag_pipeline import build_vector_store, chunk_documents, load_vector_store, resolve_persist_dir
from agent import build_agent


def load_test_questions(test_file: str = "eval/test_questions.json") -> list[dict]:
    """Load test questions from JSON file."""
    with open(test_file, "r", encoding="utf-8") as f:
        return json.load(f)


def llm_judge_score(question: str, answer: str, context: str) -> dict:
    """使用大模型作为裁判，为回答的忠实度和相关性打分 (1-5)"""
    from config import ChatGoogleGenerativeAI
    import json as _json

    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
    prompt = f"""
    You are an expert evaluator for a RAG tutor that teaches technical concepts through legal analogies. Score the given Answer from 1 to 5 on two metrics:
    1. Faithfulness: Is the answer strictly derived from the Context without hallucinating details not present?
    2. Relevance: Does the answer directly and concisely address the Question?

    Question: {question}
    Context: {context[:2000]}
    Answer: {answer}

    Output strictly ONLY a raw JSON dictionary without Markdown formatting or backticks:
    {{"faithfulness": 4, "relevance": 5}}
    """
    try:
        response = llm.invoke(prompt)
        text = response.content.replace('```json', '').replace('```', '').strip()
        return _json.loads(text)
    except Exception as e:
        print(f"[Judge Error] {e}")
        return {"faithfulness": 0, "relevance": 0}


def _extract_context_from_steps(response: dict) -> str:
    """Extract retrieved document text from agent intermediate_steps."""
    parts = []
    for step in response.get("intermediate_steps", []):
        _, observation = step
        if isinstance(observation, str) and observation.strip():
            parts.append(observation)
    return "\n\n".join(parts)


def score_answer(response: dict, expected: dict) -> dict:
    """
    Score an answer based on:
    - keyword_hit_rate: % of expected keywords found in the answer
    - source_accuracy: whether the expected source was retrieved in intermediate_steps
    """
    answer = response.get("output", "")
    answer_lower = answer.lower()

    keywords = expected.get("expected_keywords", [])
    hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
    keyword_rate = hits / len(keywords) if keywords else 0.0

    expected_source = expected.get("expected_source_contains", "")
    source_hit = False
    if expected_source:
        expected_src_lower = expected_source.lower()
        for step in response.get("intermediate_steps", []):
            action, observation = step
            if isinstance(observation, str) and expected_src_lower in observation.lower():
                source_hit = True
                break

    return {
        "keyword_hit_rate": round(keyword_rate, 2),
        "keyword_hits": hits,
        "keyword_total": len(keywords),
        "source_accuracy": source_hit,
    }


def evaluate_rag(
    agent_executor,
    test_file: str = "eval/test_questions.json",
    output_file: str = "eval/eval_results.json",
) -> dict:
    """
    Run all test questions through the agent and score each answer.
    Saves results to eval/eval_results.json.
    """
    questions = load_test_questions(test_file)
    results = []
    total_keyword_rate = 0.0
    total_source_hits = 0
    total_faithfulness = 0.0
    total_relevance = 0.0
    judge_count = 0

    print(f"\nEvaluating {len(questions)} questions...\n")

    for idx, q in enumerate(questions):
        if idx > 0:
            time.sleep(5)
        print(f"  [{q['id']}/{len(questions)}] {q['question'][:60]}...")

        try:
            start = time.time()
            response = agent_executor.invoke({"input": q["question"]})
            elapsed = time.time() - start
            answer = response.get("output", "")
        except Exception as e:
            print(f"    [ERROR] {e}")
            response = {"output": f"ERROR: {e}", "intermediate_steps": []}
            answer = response["output"]
            elapsed = 0

        scores = score_answer(response, q)
        total_keyword_rate += scores["keyword_hit_rate"]
        total_source_hits += int(scores["source_accuracy"])

        judge = {"faithfulness": 0, "relevance": 0}
        if not answer.startswith("ERROR:"):
            context = _extract_context_from_steps(response)
            if context:
                time.sleep(2)
                judge = llm_judge_score(q["question"], answer, context)
                total_faithfulness += judge.get("faithfulness", 0)
                total_relevance += judge.get("relevance", 0)
                judge_count += 1

        result = {
            "id": q["id"],
            "question": q["question"],
            "expected_topic": q["expected_topic"],
            "answer": answer[:500],
            "scores": scores,
            "llm_judge": judge,
            "time_seconds": round(elapsed, 2),
        }
        results.append(result)
        print(f"    Keywords: {scores['keyword_hits']}/{scores['keyword_total']} "
              f"| Source: {'✓' if scores['source_accuracy'] else '✗'} "
              f"| Faith: {judge['faithfulness']}/5 | Rel: {judge['relevance']}/5"
              f" | Time: {elapsed:.1f}s")

    n = len(questions)
    summary = {
        "total_questions": n,
        "avg_keyword_hit_rate": round(total_keyword_rate / n, 3) if n else 0,
        "source_accuracy_rate": round(total_source_hits / n, 3) if n else 0,
        "total_source_hits": total_source_hits,
        "avg_faithfulness": round(total_faithfulness / judge_count, 2) if judge_count else 0,
        "avg_relevance": round(total_relevance / judge_count, 2) if judge_count else 0,
        "judged_count": judge_count,
    }

    output = {"summary": summary, "results": results}

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print("EVALUATION SUMMARY")
    print(f"{'='*50}")
    print(f"Questions tested: {n}")
    print(f"Avg keyword hit rate: {summary['avg_keyword_hit_rate']:.1%}")
    print(f"Source accuracy: {summary['source_accuracy_rate']:.1%} ({total_source_hits}/{n})")
    print(f"Avg faithfulness: {summary['avg_faithfulness']}/5 ({summary['judged_count']} judged)")
    print(f"Avg relevance: {summary['avg_relevance']}/5 ({summary['judged_count']} judged)")
    print(f"Results saved to: {output_file}")

    return output


def compare_strategies(
    test_file: str = "eval/test_questions.json",
) -> None:
    """
    Build two vector stores (Strategy A and B), run the same questions on both,
    and output a comparison table.
    """
    print("=" * 60)
    print("CHUNKING STRATEGY COMPARISON")
    print("=" * 60)

    docs = load_all_documents()
    if not docs:
        print("No documents loaded. Run download_data.py first.")
        return

    results_by_strategy = {}

    for strategy in ["A", "B"]:
        print(f"\n--- Strategy {strategy} ---")
        vs = build_vector_store(docs, strategy=strategy)
        executor = build_agent(vs)

        output = evaluate_rag(
            executor,
            test_file=test_file,
            output_file=f"eval/eval_results_strategy_{strategy}.json",
        )
        results_by_strategy[strategy] = output["summary"]

    print(f"\n{'='*70}")
    print("COMPARISON TABLE")
    print(f"{'='*70}")
    print(f"{'Strategy':<10} {'Chunk Size':<12} {'Overlap':<10} {'Keyword Hit Rate':<18} {'Source Accuracy':<16}")
    print("-" * 70)
    print(f"{'A':<10} {'500':<12} {'100':<10} "
          f"{results_by_strategy['A']['avg_keyword_hit_rate']:.1%}{'':<12} "
          f"{results_by_strategy['A']['source_accuracy_rate']:.1%}")
    print(f"{'B':<10} {'800':<12} {'150':<10} "
          f"{results_by_strategy['B']['avg_keyword_hit_rate']:.1%}{'':<12} "
          f"{results_by_strategy['B']['source_accuracy_rate']:.1%}")


if __name__ == "__main__":
    print("=== Evaluation Pipeline ===\n")
    print("Running single strategy evaluation (Strategy A)...\n")

    docs = load_all_documents()
    if not docs:
        print("No documents loaded. Run download_data.py first.")
    else:
        persist_dir = resolve_persist_dir("A")
        if Path(persist_dir).exists():
            print("Loading existing vector store...")
            vs = load_vector_store(strategy="A", persist_dir=persist_dir)
        else:
            print("Building vector store from scratch...")
            vs = build_vector_store(docs, strategy="A", persist_dir=persist_dir)
        chunks = chunk_documents(docs, strategy="A")
        executor = build_agent(vs, chunks)
        evaluate_rag(executor)
