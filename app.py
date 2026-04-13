"""
Legacy Streamlit UI for the CLS Course Assistant.
Provides Chat mode (Q&A with RAG) and Quiz mode (auto-generated quizzes).
"""

import os
import re
import time
from pathlib import Path

try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "app.py is a legacy Streamlit prototype. The default supported startup "
        "path is `uvicorn server:app`; install Streamlit separately if you "
        "intentionally need the legacy UI."
    ) from exc

from config import CHROMA_PERSIST_DIR
from rag_pipeline import load_vector_store, build_vector_store
from hybrid_retriever import build_hybrid_retriever, search_by_topic
from agent import build_agent
from quiz_generator import generate_quiz
from data_loader import load_all_documents

st.set_page_config(
    page_title="CLS Course Assistant",
    page_icon="⚖️",
    layout="wide",
)

CUSTOM_CSS = """
<style>
    .stApp { max-width: 1200px; margin: 0 auto; }
    .source-box {
        background-color: #1e1e2e;
        border-left: 3px solid #89b4fa;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 6px;
        font-size: 0.85em;
        color: #cdd6f4;
        line-height: 1.5;
    }
    .source-box b {
        color: #89b4fa;
        font-size: 0.9em;
    }
    .quiz-question {
        background-color: #1e1e2e;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #45475a;
    }
    div[data-testid="stSidebar"] { background-color: #11111b; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

EXAMPLE_QUESTIONS = [
    "What is a for loop in Python?",
    "How do I perform a T-test with SciPy?",
    "What is tokenization in NLP?",
    "What does Article 1062 say about property division?",
    "Explain regression analysis for legal research.",
]


@st.cache_resource(show_spinner="Loading course materials...")
def init_backend():
    """Initialize the vector store, hybrid retriever, and agent."""
    persist_dir = f"{CHROMA_PERSIST_DIR}_strategy_A"

    if Path(persist_dir).exists():
        try:
            vs = load_vector_store(strategy="A")
            docs = load_all_documents()
            from rag_pipeline import chunk_documents
            chunks = chunk_documents(docs, strategy="A")
            hybrid = build_hybrid_retriever(vs, chunks)
            executor = build_agent(vs)
            return vs, hybrid, executor
        except Exception:
            pass

    docs = load_all_documents()
    if not docs:
        st.error("No documents found. Please run `python scripts/download_data.py` first.")
        st.stop()

    vs = build_vector_store(docs, strategy="A")
    from rag_pipeline import chunk_documents
    chunks = chunk_documents(docs, strategy="A")
    hybrid = build_hybrid_retriever(vs, chunks)
    executor = build_agent(vs)
    return vs, hybrid, executor


# --- Sidebar ---
with st.sidebar:
    st.title("⚖️ CLS Course Assistant")
    st.markdown(
        "An intelligent teaching assistant for the "
        "**Computational Legal Studies** workshop."
    )
    if os.getenv("AMICUS_SMOKE_TEST") == "1":
        st.caption("Smoke test mode: external Gemini embedding calls are disabled.")
    st.divider()

    mode = st.radio("Mode", ["💬 Chat", "📝 Quiz"], horizontal=True)

    st.divider()
    st.markdown("**Try these questions:**")
    for eq in EXAMPLE_QUESTIONS:
        if st.button(eq, key=f"ex_{eq}", use_container_width=True):
            st.session_state["prefill_question"] = eq

    st.divider()
    with st.expander("🏗️ Architecture"):
        st.markdown("""
```
Data Sources (.docx, .pdf, .ipynb, .py, .md)
  → Multi-Format Loader
  → Chunking (2 strategies)
  → Embedding (Gemini Embedding 001)
  → ChromaDB Vector Store
  → Hybrid Retrieval (Vector + BM25)
  → ReAct Agent (4 topic tools)
  → Gemini 3 Flash Preview
  → Response with Citations
```
        """)

# --- Initialize backend ---
vs, hybrid, executor = init_backend()

# --- Chat Mode ---
if mode == "💬 Chat":
    st.header("💬 Ask a Question")
    st.caption("Ask about Python, Statistics, NLP, or Legal topics from the course materials.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📎 Sources"):
                    for src in msg["sources"]:
                        st.markdown(
                            f'<div class="source-box">'
                            f'<b>{src["source"]}</b><br>{src["text"]}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

    prefill = st.session_state.pop("prefill_question", None)
    user_input = st.chat_input("Type your question here...") or prefill

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching course materials..."):
                try:
                    # Build conversation history for context
                    history_text = ""
                    past_messages = st.session_state.messages[:-1]
                    if past_messages:
                        history_lines = []
                        for msg in past_messages[-6:]:
                            role = "Student" if msg["role"] == "user" else "Amicus"
                            history_lines.append(f"{role}: {msg['content'][:200]}")
                        history_text = "\n".join(history_lines)

                    if history_text:
                        full_input = f"[CONVERSATION HISTORY - use this to determine if this is a follow-up question]\n{history_text}\n\n[CURRENT QUESTION]\n{user_input}"
                    else:
                        full_input = user_input

                    # Retry logic for API failures (503, rate limits, etc.)
                    max_retries = 3
                    result = {}
                    answer = ""
                    for attempt in range(max_retries):
                        try:
                            result = executor.invoke({"input": full_input})
                            answer = result.get("output", "Sorry, I couldn't find an answer.")
                            break  # Success — exit retry loop
                        except Exception as api_err:
                            error_str = str(api_err).lower()
                            is_retryable = any(keyword in error_str for keyword in [
                                "503", "unavailable", "overloaded", "rate limit",
                                "resource exhausted", "deadline exceeded", "high demand",
                            ])
                            if is_retryable and attempt < max_retries - 1:
                                wait_time = 2 ** attempt  # 1s, 2s, 4s
                                time.sleep(wait_time)
                                continue
                            else:
                                raise  # Non-retryable error or last attempt
                except Exception as e:
                    error_msg = str(e)
                    if "503" in error_msg or "UNAVAILABLE" in error_msg or "high demand" in error_msg.lower():
                        answer = (
                            "🪶 The AI service is temporarily busy due to high demand. "
                            "This is a temporary issue on Google's side, not a problem with Amicus.\n\n"
                            "**Please wait a moment and try again.** Your question was received — "
                            "the system just needs a few seconds to become available."
                        )
                    else:
                        answer = (
                            "🪶 I encountered an unexpected issue while searching the course materials. "
                            "Please try rephrasing your question or try again in a moment.\n\n"
                            f"*Technical detail: {error_msg[:150]}*"
                        )
                    result = {}

                # Extract sources from Agent's actual tool calls (intermediate_steps)
                sources = []
                for step in result.get("intermediate_steps", []):
                    action, observation = step
                    if isinstance(observation, str) and observation.strip() and "No results found" not in observation:
                        for block in observation.split("\n\n---\n\n"):
                            lines = block.strip().split("\n")
                            if lines and lines[0].startswith("[Source"):
                                try:
                                    header = lines[0]
                                    source_info = header.split(":", 1)[1].rsplit("]", 1)[0].strip()
                                    text_preview = "\n".join(lines[1:])[:300]
                                    sources.append({"source": source_info, "text": text_preview})
                                except (IndexError, ValueError):
                                    continue

                # Fallback: if Agent didn't use tools, use hybrid retriever
                if not sources:
                    try:
                        fallback_docs = hybrid.invoke(user_input)
                        sources = [
                            {
                                "source": doc.metadata.get("source", "unknown"),
                                "text": doc.page_content[:300],
                            }
                            for doc in fallback_docs[:4]
                        ]
                    except Exception:
                        sources = [{"source": "Course Materials", "text": "Source details unavailable. Please restart the app if this persists."}]

                # Deduplicate by source name, keep first 4
                seen = set()
                unique_sources = []
                for s in sources:
                    if s["source"] not in seen:
                        seen.add(s["source"])
                        unique_sources.append(s)
                sources = unique_sources[:4]

            answer = answer.strip()
            answer = re.sub(r'^#{1,3}\s+', '', answer, flags=re.MULTILINE)

            st.markdown(answer)

            show_sources = ("quiz mode" not in answer.lower()
                            and "not covered" not in answer.lower()
                            and "your professor or ta" not in answer.lower())
            if show_sources and sources:
                with st.expander("📎 Sources"):
                    for src in sources:
                        st.markdown(
                            f'<div class="source-box">'
                            f'<b>{src["source"]}</b><br>{src["text"]}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )

# --- Quiz Mode ---
elif mode == "📝 Quiz":
    st.header("📝 Quiz Generator")
    st.caption("Test your understanding of course concepts.")

    col1, col2 = st.columns([3, 1])
    with col1:
        quiz_topic = st.text_input(
            "Enter a topic",
            placeholder="e.g., p-value, tokenization, for loop, property division",
        )
    with col2:
        num_q = st.number_input("Questions", min_value=1, max_value=5, value=3)

    if st.button("🎲 Generate Quiz", type="primary", use_container_width=True):
        if not quiz_topic:
            st.warning("Please enter a topic first.")
        else:
            with st.spinner(f"Generating {num_q} questions about '{quiz_topic}'..."):
                quiz_text = generate_quiz(quiz_topic, vs, num_questions=num_q)
            st.markdown(quiz_text)
