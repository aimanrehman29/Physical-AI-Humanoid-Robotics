# Backend (FastAPI) — Physical AI RAG Chatbot

Starter backend for the textbook RAG chatbot using Qdrant + Cohere embeddings (LLM hookup pending).

## Setup
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Env vars (example)
```
QDRANT_URL=https://your-qdrant:6333
QDRANT_API_KEY=
COLLECTION_NAME=humanoid_ai_book
COHERE_API_KEY=
EMBED_MODEL=embed-english-v3.0
LLM_MODEL=           # optional, not used yet
ALLOWED_ORIGINS=*
```

## Endpoints (placeholder)
- `GET /health` — health check.
- `POST /chat` — accepts `{question, session_id?}`; retrieval-backed placeholder (Cohere embed + Qdrant). Swap in real LLM call once keys are set.
- `POST /feedback` — accepts `{question, answer, chunk_ids, sentiment, session_id?}`; logs feedback (to be wired later).

## TODO
- Ingestion script: fetch sitemap/MDX, chunk, embed, upsert to Qdrant with metadata.
- Retrieval + LLM pipeline in `/chat` (sanitize, embed, retrieve, prompt, stream).
- Optional storage for feedback and ingestion runs.
- Streaming responses and better error handling.
