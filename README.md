---
title: Amicus
emoji: ⚖️
colorFrom: indigo
colorTo: gray
sdk: docker
pinned: false
---

<div align="center">

# ⚖️ Amicus

**A RAG teaching assistant that explains code and statistics through legal analogies.**

Built with LangChain ReAct Agent · Gemini · ChromaDB<br/>
Deployed on Hugging Face Spaces

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face-yellow.svg)](https://huggingface.co/spaces/skye210/cls-course-assistant)

<br/>

<img src="docs/assets/hero.png" alt="Amicus landing page" width="800">

</div>

## What is Amicus?

Amicus is a RAG-powered assistant for a Computational Legal Studies workshop. It answers questions about Python, statistics, NLP, and Chinese law using course materials as its knowledge base. Answers are framed with legal-domain analogies to match the audience—law students with no prior programming experience.

## Features

### 1. Pedagogical Answers
The agent maps technical concepts to legal frameworks familiar to the target audience. For example, p-values are explained through the lens of "burden of proof," and Python is compared to a "Model Code" that standardizes how instructions are written and executed.

<div align="center">
  <img src="docs/assets/pedagogy.png" alt="Chat answer with legal analogies" width="800">
</div>

<br/>

### 2. Source Grounding
Answers include source cards that cite the original material—PDF page numbers, notebook sections, or textbook chapters. Users can expand or collapse the grounding panel to verify claims against the course content.

<div align="center">
  <img src="docs/assets/grounding.png" alt="Source citation cards" width="800">
</div>

<br/>

### 3. Quiz Mode
Users can generate topic-specific multiple-choice questions. After answering, the system shows whether the selection was correct or incorrect, provides an explanation, and cites the source material used to construct the question.

<div align="center">
  <img src="docs/assets/quiz.png" alt="Quiz with feedback" width="800">
</div>

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

| Layer | Stack |
|-------|-------|
| LLM | Gemini 3 Flash Preview |
| Embeddings | Gemini Embedding 001 |
| Orchestration | LangChain ReAct Agent (4 topic-specific tools) |
| Vector Store | ChromaDB |
| Retrieval | Hybrid — vector similarity + BM25 keyword search |
| Serving | FastAPI + Uvicorn |
| Frontend | Vanilla HTML / CSS / JS |

## Evaluation

18-question benchmark across Python, Statistics, NLP, and Chinese Law:

| Metric | Score |
|--------|-------|
| Keyword Hit Rate | 69.4% |
| Source Accuracy | 66.7% (12/18) |
| Relevance | 3.94 / 5 (LLM Judge) |
| Faithfulness | 2.59 / 5 (LLM Judge) |

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

# 3. Collect course data
python scripts/download_data.py

# 4. Start the server
uvicorn server:app --host 0.0.0.0 --port 7860 --reload
```

Open [http://127.0.0.1:7860](http://127.0.0.1:7860).

### Deploy to Hugging Face Spaces

1. Create a Docker Space.
2. Add remote and push:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/your-space-name
   git push hf main
   ```
3. Add `GOOGLE_API_KEY` to Space Secrets.

## License

Educational use. Course materials are sourced from publicly available, CC-licensed resources.
