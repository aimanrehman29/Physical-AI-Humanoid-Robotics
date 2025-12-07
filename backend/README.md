# Backend (FastAPI) — Physical AI RAG Chatbot

This is a starter backend for the RAG chatbot. It wires FastAPI, config/env handling, and placeholder endpoints. Retrieval, embeddings, Qdrant, Neon, and LLM calls still need to be implemented.

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
QDRANT_API_KEY=...
POSTGRES_URL=postgresql+psycopg://user:pass@neon-host/db
EMBED_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=*
```

## Endpoints (placeholders)
- `GET /health` — health check.
- `POST /chat` — accepts `{question, session_id?}`; returns a placeholder answer (wire RAG here).
- `POST /feedback` — accepts `{question, answer, chunk_ids, sentiment, session_id?}`; logs feedback (wire Postgres insert here).

## TODO
- Add ingestion script: parse MD/MDX, chunk, embed, upsert to Qdrant with metadata.
- Add retrieval + LLM pipeline in `/chat` (sanitize, embed, retrieve, prompt, stream).
- Add Postgres storage for feedback and ingestion runs.
- Add streaming responses and proper error handling.
