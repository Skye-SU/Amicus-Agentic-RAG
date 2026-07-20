---
title: Amicus
emoji: ⚖️
colorFrom: indigo
colorTo: gray
sdk: docker
pinned: false
---

# ⚖️ Amicus

**A RAG teaching assistant that explains code and statistics through legal analogies.**

Built with LangChain ReAct Agent · Gemini · ChromaDB  

Deployed on Hugging Face Spaces

[Live Demo](https://huggingface.co/spaces/skye210/cls-course-assistant)

## What is Amicus?

Amicus is an experimental RAG tutor that explains programming, statistics, and NLP through legal analogies. It's built as a teaching demo for how domain-anchored pedagogy and retrieval grounding can make technical topics more accessible to learners with a legal background — law students, paralegals, and legal professionals stepping into computational methods. Its reference library is assembled from publicly available, CC-licensed educational resources and primary legal authorities (e.g., Chinese Civil Code articles).

## Features

### 1. Pedagogical Answers

The agent maps technical concepts to legal frameworks familiar to the target audience. For example, p-values are explained through the lens of "burden of proof," and Python is compared to a "Model Code" that standardizes how instructions are written and executed.

### 2. Source Grounding

Answers include source cards that cite the original material—PDF page numbers, notebook sections, or textbook chapters. Users can expand or collapse the grounding panel to verify claims against the underlying reference.

### 3. Quiz Mode

Users can generate topic-specific multiple-choice questions. After answering, the system shows whether the selection was correct or incorrect, provides an explanation, and cites the source material used to construct the question.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Vanilla    │────>│   FastAPI     │────>│    ChromaDB      │
│   HTML/JS    │<────│   + Uvicorn   │<────│  (Vector Store)  │
└──────────────┘     └──────┬───────┘     └──────────────────┘
                            │
                     ┌──────┴───────┐
                     │  ReAct Agent │
                     │  (LangChain) │
                     │  4 topic     │
                     │  tools       │
                     └──────┬───────┘
                            │
                     ┌──────┴───────┐
                     │   Gemini 3   │
                     │ Flash Preview│
                     └──────────────┘
```


| Layer         | Stack                                            |
| ------------- | ------------------------------------------------ |
| LLM           | Gemini 3 Flash Preview                           |
| Embeddings    | Gemini Embedding 001                             |
| Orchestration | LangChain ReAct Agent (4 topic-specific tools)   |
| Vector Store  | ChromaDB                                         |
| Retrieval     | Hybrid — vector similarity + BM25 keyword search |
| Serving       | FastAPI + Uvicorn                                |
| Frontend      | Vanilla HTML / CSS / JS                          |


## Evaluation

18-question benchmark across Python, Statistics, NLP, and Chinese Law:


| Metric           | Score                |
| ---------------- | -------------------- |
| Keyword Hit Rate | 69.4%                |
| Source Accuracy  | 66.7% (12/18)        |
| Relevance        | 3.94 / 5 (LLM Judge) |
| Faithfulness     | 2.59 / 5 (LLM Judge) |


The faithfulness score reflects a design trade-off: the agent is configured to generate explanatory analogies and inferences rather than repeat source text verbatim. Source cards are provided with each answer so users can cross-check against the original material.

## Setup

### Local Development

```bash
# 1. Install dependencies
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Add GOOGLE_API_KEY=your-key-here

# 3. Collect public reference data
python scripts/download_data.py --force

# 4. Start the server
uvicorn server:app --host 0.0.0.0 --port 7860 --reload
```

Open [http://127.0.0.1:7860](http://127.0.0.1:7860).

If cloned files contain Git LFS pointers instead of real PDFs, `scripts/download_data.py --force`
refreshes the public reference materials. The FastAPI startup path also rejects pointer-based
ChromaDB files and rebuilds the vector store from real reference documents.

`app.py` is retained only as a legacy compatibility message. The supported application entry point
is `server.py` plus the static frontend in `static/`.

### Portfolio Demo Guardrails

For a public resume or PI-review demo, use a dedicated Gemini API project with a small prepaid
balance and auto-reload disabled. The app also ships with conservative default limits:

| Setting | Default |
| --- | ---: |
| Chat requests per visitor per minute | 3 |
| Quiz requests per visitor per minute | 1 |
| Chat requests globally per hour | 20 |
| Quiz requests globally per hour | 6 |
| Chat requests globally per rolling day | 25 |
| Quiz requests globally per rolling day | 8 |
| Chat requests per visitor per rolling day | 20 |
| Quiz requests per visitor per rolling day | 6 |
| Agent iterations per answer | 4 |
| Chat/direct-RAG output token cap | 900 |
| Quiz output token cap | 1200 |

All of these can be adjusted through environment variables in `.env.example` without changing code.
Monitor Gemini spending from Google AI Studio Dashboard > Usage and Billing.

### Deploy to Hugging Face Spaces

1. Create a Docker Space.
2. Add remote and push:
  ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/your-space-name
   git push hf main
  ```
3. Add `GOOGLE_API_KEY` to Space Secrets.
4. The Docker build runs `scripts/download_data.py` before startup, so the Space does not depend on
   Git LFS objects being present in the clone.

## License

Educational use. Reference materials are sourced from publicly available, CC-licensed resources.
