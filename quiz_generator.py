"""
Quiz generation feature: generates multiple-choice questions from the reference library.
"""

from langchain_core.documents import Document
from langchain_classic.prompts import PromptTemplate
from config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE, ChatGoogleGenerativeAI
from hybrid_retriever import search_by_topic


QUIZ_PROMPT = PromptTemplate(
    input_variables=["topic", "num_questions", "context"],
    template="""Based on the following reference materials about "{topic}", generate {num_questions} multiple-choice quiz questions.

REFERENCE MATERIALS:
{context}

STRICT OUTPUT FORMAT — you MUST follow this format EXACTLY for each question, with no deviations:

---
Question: [Write the full question text here on a single line]

A) [Option A text]
B) [Option B text]
C) [Option C text]
D) [Option D text]

Correct Answer: [Single letter: A, B, C, or D]

Explanation: [Brief explanation of why this is the correct answer, referencing the reference materials]

Source: [Document name and section/page where this concept is covered]
---

RULES:
- Separate each question with a line of three dashes (---).
- Each question MUST have exactly 4 options labeled A), B), C), D).
- The "Correct Answer:" line MUST contain exactly one letter (A, B, C, or D), nothing else.
- Do NOT use markdown formatting (no **, no ## headers, no numbered lists).
- Do NOT add any extra text, commentary, or introductions before or after the questions.
- Start your output directly with --- followed by the first question.

QUALITY REQUIREMENTS (VERY IMPORTANT):
- Learners have a legal background and little or no programming experience. Use PLAIN ENGLISH.
  BAD question: "In which type of numerical analysis are p-values relevant?"
  GOOD question: "When would you most likely use a p-value in legal research?"
- Frame questions around LEGAL research scenarios whenever possible.
  BAD: "What does a for loop do?"
  GOOD: "A researcher wants to count how many times the word 'negligence' appears in 100 court rulings. Which Python concept would be most useful?"
- Each Explanation MUST have TWO parts: (1) state the correct answer clearly, (2) explain WHY using a concrete legal example.
  BAD explanation: "The reference says p-values relate to comparing means."
  GOOD explanation: "A p-value tells you whether a difference is statistically meaningful. For example, if male defendants get 2-year longer sentences on average, the p-value tells you whether this gap is real or just random variation in the data."
- Wrong options must be PLAUSIBLE but clearly wrong. Do NOT use absurd distractors like "updating database records for page rank" that make the quiz look unprofessional.
- Questions should test CONCEPTUAL understanding, not trivia or memorization.
""",
)


def generate_quiz(
    topic: str,
    vectorstore,
    llm=None,
    num_questions: int = 3,
) -> str:
    """
    Generate a quiz on the given topic.
    1. Retrieve relevant reference material
    2. Ask LLM to generate multiple-choice questions
    3. Return formatted quiz string
    """
    if llm is None:
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE + 0.2,  # slightly more creative for quiz gen
            google_api_key=GOOGLE_API_KEY,
        )

    topic_keywords = {
        "python": ["python", "loop", "function", "variable", "list", "dict", "class", "def", "for", "while", "string"],
        "statistics": ["statistic", "p-value", "t-test", "regression", "hypothesis", "probability", "mean", "variance"],
        "nlp": ["nlp", "tokeniz", "sentiment", "ner", "entity", "spacy", "nltk", "text processing", "pos tag"],
        "legal": ["legal", "law", "article", "court", "divorce", "property", "custody", "statute"],
    }
    topic_to_filter = {
        "python": "python",
        "statistics": "statistics",
        "nlp": "nlp",
        "legal": "legal_knowledge",
    }

    search_topic = None
    topic_lower = topic.lower()
    for cat, keywords in topic_keywords.items():
        if cat in topic_lower or any(kw in topic_lower for kw in keywords):
            search_topic = topic_to_filter[cat]
            break
    if search_topic is None:
        search_topic = "python"

    results = search_by_topic(vectorstore, topic, search_topic, k=6)

    if not results:
        return f"No reference materials found for topic '{topic}'. Available topics: python, statistics, nlp, legal."

    context = "\n\n---\n\n".join(
        f"[{doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in results
    )

    try:
        prompt_text = QUIZ_PROMPT.format(
            topic=topic,
            num_questions=num_questions,
            context=context,
        )
        response = llm.invoke(prompt_text)
        return response.content
    except Exception as e:
        return f"[ERROR] Quiz generation failed: {e}"


if __name__ == "__main__":
    from data_loader import load_all_documents
    from rag_pipeline import build_vector_store

    print("=== Quiz Generator Standalone Test ===\n")

    docs = load_all_documents()
    if not docs:
        print("No documents loaded. Run download_data.py first.")
    else:
        vs = build_vector_store(docs, strategy="A")

        for topic in ["python", "statistics"]:
            print(f"\n{'='*60}")
            print(f"Generating quiz for: {topic}")
            print("=" * 60)
            quiz = generate_quiz(topic, vs, num_questions=2)
            print(quiz)
