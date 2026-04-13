"""
Hybrid Retriever: combines vector similarity search with BM25 keyword matching.
"""

import re

from langchain_core.documents import Document
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma

from config import (
    DEFAULT_RETRIEVAL_K,
    GLOBAL_RELEVANCE_THRESHOLD,
    HYBRID_RETRIEVER_WEIGHTS,
    TOPIC_RELEVANCE_THRESHOLD,
)

ARTICLE_REFERENCE_PATTERNS = (
    re.compile(r"\bart[_\s]*(\d{3,4})\b", re.I),
    re.compile(r"\barticle\s+(\d{3,4})\b", re.I),
    re.compile(r"\bcivil code(?:\s+book\s+\w+)?(?:\s+(?:art(?:icle)?)?)?\s*(\d{3,4})\b", re.I),
    re.compile(r"\b(\d{3,4})\s+of\s+the\s+civil code\b", re.I),
)


def build_hybrid_retriever(
    vectorstore: Chroma,
    documents: list[Document],
    weights: list[float] = None,
    k: int = None,
) -> EnsembleRetriever:
    """
    Combine vector retriever (semantic similarity) and BM25 retriever (keyword matching).
    - Vector retriever: good for paraphrased questions
    - BM25 retriever: good for exact terms like 'Art_1062'
    Returns an EnsembleRetriever.
    """
    if weights is None:
        weights = HYBRID_RETRIEVER_WEIGHTS
    if k is None:
        k = DEFAULT_RETRIEVAL_K

    vector_retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": max(k, 6), "score_threshold": TOPIC_RELEVANCE_THRESHOLD},
    )

    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = k

    hybrid = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=weights,
    )
    print(f"Hybrid retriever built: weights={weights}, k={k}")
    return hybrid


def _document_key(doc: Document) -> tuple:
    metadata = doc.metadata
    return (
        metadata.get("source"),
        metadata.get("format"),
        metadata.get("topic"),
        metadata.get("page_number"),
        metadata.get("section_title"),
        metadata.get("cell_index"),
        metadata.get("article_id"),
        doc.page_content[:160],
    )


def _dedupe_documents(documents: list[Document]) -> list[Document]:
    seen = set()
    unique = []
    for doc in documents:
        key = _document_key(doc)
        if key in seen:
            continue
        seen.add(key)
        unique.append(doc)
    return unique


def _vector_search(
    vectorstore: Chroma,
    query: str,
    *,
    k: int,
    threshold: float,
    filter_by: dict | None = None,
) -> list[Document]:
    try:
        search_kwargs = {"k": max(k, 6)}
        if filter_by:
            search_kwargs["filter"] = filter_by
        scored = vectorstore.similarity_search_with_relevance_scores(
            query,
            **search_kwargs,
        )
        return [doc for doc, score in scored if score >= threshold]
    except Exception as e:
        scope = f"filter {filter_by}" if filter_by else "global"
        print(f"[WARN] Vector search failed for {scope}: {e}")
        return []


def extract_article_reference(query: str) -> dict | None:
    raw_query = query or ""
    for pattern in ARTICLE_REFERENCE_PATTERNS:
        match = pattern.search(raw_query)
        if match:
            article_number = match.group(1)
            return {
                "article_number": article_number,
                "article_id": f"Art_{article_number}",
            }
    return None


def search_legal_authority(
    documents: list[Document],
    query: str,
    *,
    k: int = DEFAULT_RETRIEVAL_K,
) -> list[Document]:
    article_ref = extract_article_reference(query)
    if not article_ref:
        return []

    article_id = article_ref["article_id"]
    article_number = article_ref["article_number"]
    legal_docs = [doc for doc in documents if doc.metadata.get("topic") == "legal_knowledge"]
    if not legal_docs:
        return []

    exact_matches = [
        doc for doc in legal_docs
        if str(doc.metadata.get("article_id", "")).lower() == article_id.lower()
    ]
    if exact_matches:
        return _dedupe_documents(exact_matches)[:k]

    reference_matches = []
    for doc in legal_docs:
        haystack = " ".join(
            [
                doc.page_content.lower(),
                str(doc.metadata.get("article_id", "")).lower(),
                str(doc.metadata.get("source", "")).lower(),
            ]
        )
        score = 0
        if article_id.lower() in haystack:
            score += 100
        if f"art {article_number}" in haystack:
            score += 80
        if f"article {article_number}" in haystack:
            score += 80
        if article_number in haystack:
            score += 20
        if score:
            reference_matches.append((score, doc))

    reference_matches.sort(key=lambda item: item[0], reverse=True)
    return _dedupe_documents([doc for score, doc in reference_matches if score > 0])[:k]


def keyword_search(
    documents: list[Document],
    query: str,
    *,
    k: int = DEFAULT_RETRIEVAL_K,
) -> list[Document]:
    if not documents:
        return []

    retriever = BM25Retriever.from_documents(documents)
    retriever.k = max(k, 1)

    try:
        results = retriever.invoke(query)
    except Exception as e:
        print(f"[WARN] BM25 search failed: {e}")
        return []

    query_terms = {
        term
        for term in re.findall(r"[a-z0-9_]+", query.lower())
        if len(term) > 2
    }
    ranked = []
    for doc in results:
        haystack = " ".join(
            [
                doc.page_content.lower(),
                str(doc.metadata.get("source", "")).lower(),
                str(doc.metadata.get("section_title", "")).lower(),
                str(doc.metadata.get("article_id", "")).lower(),
            ]
        )
        overlap = sum(1 for term in query_terms if term in haystack)
        ranked.append((overlap, doc))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return _dedupe_documents([doc for overlap, doc in ranked if overlap > 0][:k])


def search_by_topic(
    vectorstore: Chroma,
    query: str,
    topic: str,
    k: int = 3,
    topic_documents: list[Document] | None = None,
    all_documents: list[Document] | None = None,
) -> list[Document]:
    """Search within a topic, then degrade gracefully to broader lexical/global search."""
    topic_documents = topic_documents or []
    all_documents = all_documents or topic_documents

    if topic == "legal_knowledge":
        exact_authority = search_legal_authority(topic_documents or all_documents, query, k=k)
        if exact_authority:
            return exact_authority[:k]

    topic_vector_results = _vector_search(
        vectorstore,
        query,
        k=k,
        threshold=TOPIC_RELEVANCE_THRESHOLD,
        filter_by={"topic": topic},
    )
    local_results = list(topic_vector_results)
    if topic_documents:
        if len(local_results) < k:
            local_results.extend(keyword_search(topic_documents, query, k=k))

    combined = _dedupe_documents(local_results)
    if topic_vector_results and len(combined) >= k:
        return combined[:k]

    global_results = _vector_search(
        vectorstore,
        query,
        k=max(k, 4),
        threshold=GLOBAL_RELEVANCE_THRESHOLD,
    )
    if all_documents:
        if len(global_results) < k:
            global_results.extend(keyword_search(all_documents, query, k=max(k, 4)))

    return _dedupe_documents(combined + global_results)[:k]


if __name__ == "__main__":
    from data_loader import load_all_documents
    from rag_pipeline import build_vector_store, chunk_documents

    print("=== Hybrid Retriever Standalone Test ===\n")

    docs = load_all_documents()
    if not docs:
        print("No documents loaded. Run download_data.py first.")
    else:
        vs = build_vector_store(docs, strategy="A")
        chunks = chunk_documents(docs, strategy="A")

        print("\n--- Testing Hybrid Retriever ---")
        hybrid = build_hybrid_retriever(vs, chunks)

        test_queries = [
            "What is a for loop in Python?",
            "Explain p-value in statistics",
            "How does tokenization work in NLP?",
            "Art_1062 property division",
        ]

        for q in test_queries:
            print(f"\nQuery: {q}")
            results = hybrid.invoke(q)
            for i, r in enumerate(results[:2]):
                print(f"  [{i+1}] ({r.metadata.get('topic', '?')}) {r.page_content[:80]}...")

        print("\n--- Testing Topic-Filtered Search ---")
        results = search_by_topic(vs, "What is a variable?", "python", k=2, all_documents=chunks)
        print(f"\nTopic 'python' results: {len(results)}")
        for r in results:
            print(f"  {r.page_content[:80]}...")
