"""
RAG Pipeline: chunking, embedding, and vector store construction.
Supports two chunking strategies for comparison.
"""

import hashlib
import os
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from config import (
    GOOGLE_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    CHUNK_STRATEGY_A,
    CHUNK_STRATEGY_B,
    CHINESE_SEPARATORS,
)

SMOKE_TEST_ENV_VAR = "AMICUS_SMOKE_TEST"
SMOKE_TEST_PERSIST_DIR = "./.smoke_chroma_db"


class DeterministicSmokeEmbeddings:
    """Offline embeddings for startup smoke tests."""

    def __init__(self, size: int = 64):
        self.size = size

    def _embed_text(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = []
        while len(values) < self.size:
            for byte in digest:
                values.append((byte / 127.5) - 1.0)
                if len(values) >= self.size:
                    break
            digest = hashlib.sha256(digest).digest()
        return values

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)


def smoke_test_enabled() -> bool:
    return os.getenv(SMOKE_TEST_ENV_VAR) == "1"


def resolve_persist_dir(strategy: str, persist_dir: str | os.PathLike[str] | None = None) -> str:
    if persist_dir is not None:
        return str(persist_dir)

    base_dir = SMOKE_TEST_PERSIST_DIR if smoke_test_enabled() else CHROMA_PERSIST_DIR
    return f"{base_dir}_strategy_{strategy}"


def get_persist_path(
    strategy: str,
    persist_dir: str | os.PathLike[str] | None = None,
) -> Path:
    """Return the canonical persist path for a vector store strategy."""
    return Path(resolve_persist_dir(strategy, persist_dir))


def vector_store_exists(
    strategy: str,
    persist_dir: str | os.PathLike[str] | None = None,
) -> bool:
    """Report whether the canonical vector store path already exists."""
    return get_persist_path(strategy, persist_dir).exists()


def get_text_splitter(strategy: str = "A") -> RecursiveCharacterTextSplitter:
    """Get a text splitter for the given strategy."""
    if strategy == "A":
        params = CHUNK_STRATEGY_A
        separators = ["\n\n", "\n", "。", ".", " "]
    elif strategy == "B":
        params = CHUNK_STRATEGY_B
        separators = ["\n\n", "\n", "。", ".", "；", ";", " "]
    else:
        raise ValueError(f"Unknown strategy: {strategy}. Use 'A' or 'B'.")

    return RecursiveCharacterTextSplitter(
        chunk_size=params["chunk_size"],
        chunk_overlap=params["chunk_overlap"],
        separators=separators,
        length_function=len,
    )


def chunk_documents(documents: list[Document], strategy: str = "A") -> list[Document]:
    """Split documents into chunks using the specified strategy."""
    from langchain_text_splitters import Language

    code_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=800,
        chunk_overlap=150,
    )
    text_splitter = get_text_splitter(strategy)

    code_docs = [d for d in documents if d.metadata.get("format") in ("py", "ipynb")]
    text_docs = [d for d in documents if d.metadata.get("format") not in ("py", "ipynb")]

    chunks = text_splitter.split_documents(text_docs) + code_splitter.split_documents(code_docs)
    print(f"Strategy {strategy}: {len(documents)} documents → {len(chunks)} chunks")
    return chunks


def get_embeddings():
    """Create the embedding model instance."""
    if smoke_test_enabled():
        return DeterministicSmokeEmbeddings()

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )


def build_vector_store(
    documents: list[Document],
    strategy: str = "A",
    persist_dir: str | None = None,
) -> Chroma:
    """
    Build and persist a ChromaDB vector store.
    Uses batched embedding to avoid API rate limits (3000/min).
    """
    import time

    persist_path = get_persist_path(strategy, persist_dir)
    persist_path.mkdir(parents=True, exist_ok=True)

    print(f"\nBuilding vector store (Strategy {strategy})...")
    chunks = chunk_documents(documents, strategy)

    if not chunks:
        print("[WARN] No chunks to embed.")
        return None

    embeddings = get_embeddings()
    batch_size = 2500  # Under the 3000/min API limit

    try:
        if len(chunks) <= batch_size:
            # Small enough to do in one shot
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=str(persist_path),
                collection_name=f"cls_course_strategy_{strategy}",
            )
        else:
            # Batch to avoid rate limits
            print(f"  Batching {len(chunks)} chunks in groups of {batch_size}...")
            first_batch = chunks[:batch_size]
            vectorstore = Chroma.from_documents(
                documents=first_batch,
                embedding=embeddings,
                persist_directory=str(persist_path),
                collection_name=f"cls_course_strategy_{strategy}",
            )
            print(f"  Batch 1/{(len(chunks) - 1) // batch_size + 1}: {len(first_batch)} chunks embedded.")

            for i in range(batch_size, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                batch_num = i // batch_size + 1
                total_batches = (len(chunks) - 1) // batch_size + 1
                print(f"  Waiting 60s for API quota reset...")
                time.sleep(60)
                print(f"  Batch {batch_num}/{total_batches}: embedding {len(batch)} chunks...")
                vectorstore.add_documents(batch)
                print(f"  Batch {batch_num}/{total_batches}: done.")

        print(f"Vector store built: {len(chunks)} chunks stored at {persist_path}")
        return vectorstore
    except Exception as e:
        print(f"[ERROR] Failed to build vector store: {e}")
        raise


def load_vector_store(
    strategy: str = "A",
    persist_dir: str | None = None,
) -> Chroma:
    """Load an existing ChromaDB vector store."""
    persist_path = get_persist_path(strategy, persist_dir)
    persist_path.mkdir(parents=True, exist_ok=True)

    embeddings = get_embeddings()
    return Chroma(
        persist_directory=str(persist_path),
        embedding_function=embeddings,
        collection_name=f"cls_course_strategy_{strategy}",
    )


if __name__ == "__main__":
    from data_loader import load_all_documents

    print("=== RAG Pipeline Standalone Test ===\n")

    docs = load_all_documents()
    if not docs:
        print("No documents loaded. Run download_data.py first.")
    else:
        for strategy in ["A", "B"]:
            print(f"\n--- Testing Strategy {strategy} ---")
            chunks = chunk_documents(docs, strategy)
            print(f"  Sample chunk: {chunks[0].page_content[:150]}...")
            print(f"  Chunk metadata: {chunks[0].metadata}")

        print("\nBuilding vector store with Strategy A...")
        vs = build_vector_store(docs, strategy="A")
        if vs:
            results = vs.similarity_search("What is a variable in Python?", k=3)
            print(f"\nTest query results ({len(results)} hits):")
            for i, r in enumerate(results):
                print(f"  [{i+1}] {r.page_content[:100]}...")
                print(f"       Source: {r.metadata.get('source', 'N/A')}")
