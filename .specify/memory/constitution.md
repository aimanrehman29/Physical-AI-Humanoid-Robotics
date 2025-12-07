# Physical AI & Humanoid Robotics — RAG Chatbot Constitution

## Core Principles

### P1. Scope-bound answers
Answer strictly from the textbook corpus (chapters and content-ops). If out of scope or low confidence, say “not covered” and point to relevant chapters.

### P2. Retrieval-first with citations
Always retrieve before generating; every answer must cite chunks (chapter + section/anchor). No free-form hallucinations.

### P3. Safety and hygiene
Sanitize inputs for prompt injection; refuse unsafe/off-topic requests. Apply output filters to avoid PII leakage, abuse, or ungrounded execution advice.

### P4. Observability and feedback
Log queries, retrieved chunk IDs, latency, refusals, and feedback. Use feedback to refine chunking, prompts, and filters.

### P5. Performance and cost
Prefer small, fast embeddings (e.g., MiniLM/bge-small) and stream responses. Keep latency and cost low.

### P6. Maintainability
Keep components swappable: FastAPI backend, Qdrant for vectors, Neon Postgres for metadata/feedback. All config via env vars; no hardcoded secrets.

## Architecture & Constraints

- Frontend: Docusaurus chat widget that streams answers, shows citations, and links to chapter anchors.
- Backend: FastAPI with `/chat` (RAG), `/feedback`, `/ingest` (batch). Stateless by default; optional short-lived session context.
- Retrieval: Qdrant vector store with chunk metadata (chapter, path, heading, anchor). Chapter-aware filters when mentioned.
- Metadata/Logs: Neon serverless Postgres for feedback, usage logs, and run metadata.
- Models: Small embeddings; LLM chosen by env (e.g., GPT-4o-mini, Claude Haiku/Sonnet). Prompts enforce scope and citation.
- Safety: Input sanitization, prompt-injection checks, output guardrails. Refuse or deflect when outside corpus or unsafe.

## Workflow & Quality Gates

- Ingestion: Parse MD/MDX, chunk with overlap, embed, upsert to Qdrant; tag with content hash/version.
- Testing: Smoke retrieval, citation presence, refusal on out-of-scope queries, and latency budget.
- Deployment: Set env (`QDRANT_URL/KEY`, `POSTGRES_URL`, `EMBED_MODEL`, `LLM_MODEL`), run build/tests, deploy API; Docusaurus points to the API URL.
- Monitoring: Track p95 latency, errors/refusals, feedback scores; alert on missing citations or elevated errors.

## Governance

This constitution governs the RAG chatbot integration. Changes to scope, safety policy, or architecture require an explicit amendment and review. Releases must honor these principles; ungrounded answers, missing citations, or unsafe outputs are blockers.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
