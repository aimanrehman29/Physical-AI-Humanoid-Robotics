# Tasks: RAG Chatbot for Physical AI Textbook

## Setup
- [ ] Create FastAPI project skeleton with endpoints `/chat`, `/feedback`, `/ingest`.
- [ ] Add config/env handling (`QDRANT_URL/KEY`, `POSTGRES_URL`, `EMBED_MODEL`, `LLM_MODEL`, `ALLOWED_ORIGINS`).
- [ ] Add CORS and request logging middleware.

## Ingestion & Storage
- [ ] Write ingestion script: parse `textbook/docs/**` MD/MDX, normalize, chunk with overlap, add metadata (chapter, path, heading, anchor, hash).
- [ ] Embed chunks (MiniLM/bge-small) and upsert to Qdrant (idempotent by hash/ID).
- [ ] Create Neon Postgres tables: `ingestion_runs` (hash/version, counts, timestamps), `feedback` (query, answer, chunk_ids, sentiment, ts), `usage_logs` (optional).
- [ ] Run initial ingestion; verify counts and sample retrieval.

## Retrieval & RAG Pipeline
- [ ] Implement query embed → Qdrant top-k retrieval with chapter filter (if mentioned).
- [ ] Build grounded prompt with system guardrails + citations; enforce “don’t guess”.
- [ ] Call LLM (streaming) and return answer with 2–4 citations (chapter + anchor).
- [ ] Add refusal path for low-confidence/no chunks/out-of-scope.
- [ ] Add safety filters (prompt-injection check, length limits, basic PII/abuse filter).

## Feedback & Observability
- [ ] Implement `/feedback` to store thumbs up/down with query, answer, chunk IDs, timestamp in Postgres.
- [ ] Log retrieval latency, chunk IDs, refusals, and errors; add basic metrics counters.

## Frontend (Docusaurus)
- [ ] Add chat widget component: send to `/chat`, stream responses, display citations with links, show errors/refusals.
- [ ] Add feedback controls wired to `/feedback`.
- [ ] Style widget to match site theme; ensure mobile responsiveness.

## Testing
- [ ] Smoke: ingestion idempotency (re-run doesn’t duplicate), retrieval returns expected chunk, out-of-scope refusal works, citations present.
- [ ] Latency check: p95 ≤ 2.5s for typical queries (excluding cold starts).
- [ ] Manual UI test on Docusaurus page: send in-scope and out-of-scope queries, click citations, submit feedback.

## Deploy
- [ ] Configure env vars for Qdrant/Neon/LLM in deployment.
- [ ] Deploy backend (FastAPI) and frontend (Docusaurus/Vercel) pointing to the API URL.
- [ ] Document runbook for re-ingest when docs change.
