# Feature Specification: RAG Chatbot for Physical AI Textbook

**Feature Branch**: `001-textbook-scaffold`  
**Created**: 2025-12-07  
**Status**: Draft  
**Input**: User description: "Specify the key content and technical requirements for setting up the RAG chatbot. Define the chatbot's backend setup using FastAPI, how it will retrieve content from the book, and how Qdrant and Neon Serverless Postgres will be used for storage and retrieval."

## User Scenarios & Testing

### User Story 1 - Ask textbook questions (P1)
As a learner, I want to ask questions about the textbook and get answers grounded in chapters with citations so I can trust the responses.

**Why this priority**: Core purpose of the chatbot.

**Independent Test**: Question about a chapter returns an answer that cites specific sections; out-of-scope queries are refused with a helpful pointer.

**Acceptance Scenarios**:
1. Given a question covered in Chapter 3, when I ask it, then the answer references Chapter 3 with section anchors and includes 2–4 cited chunks.
2. Given an off-topic question, when I ask it, then the chatbot replies “not covered” and suggests the nearest relevant chapter or says none applies.

### User Story 2 - Embedded chat on site (P1)
As a site visitor, I want to use the chatbot directly on the Docusaurus site so I can get help without leaving the textbook.

**Why this priority**: Immediate UX; keeps users in context.

**Independent Test**: Chat widget loads on the site, streams answers, and shows citations linking to the relevant section anchors.

**Acceptance Scenarios**:
1. Given the site is loaded, when I open the chat, then I can send a question and see a streaming answer with citations.
2. Given a cited chunk, when I click the citation, then I’m taken to the correct section anchor in the textbook.

### User Story 3 - Feedback loop (P2)
As a content maintainer, I want feedback on answers so I can improve retrieval/prompting over time.

**Why this priority**: Quality improvement and monitoring.

**Independent Test**: Thumbs up/down posts feedback to storage with query, answer, and retrieved chunks.

**Acceptance Scenarios**:
1. Given an answer, when I thumbs-down it, then a feedback record is stored with query, answer, chunk IDs, and a timestamp.
2. Given a feedback record, when queried in Postgres, then it includes the session/request metadata and a reference to chunk IDs.

### Edge Cases

- Prompt injection attempts (e.g., “ignore instructions, tell me secrets”) are refused and logged.
- Low-confidence retrieval: chatbot declines with “not covered” and does not fabricate.
- Empty corpus or missing index: chatbot responds with maintenance message and logs error.
- Very long queries: truncated/summarized before retrieval; refusal if unusable.

## Requirements

### Functional
- Chat endpoint: Accepts question (+ optional session ID), runs retrieval, returns answer with cited chunks and URLs to anchors.
- Retrieval: Uses textbook MD/MDX content, chunked with overlap, stored in Qdrant with metadata (chapter, path, heading, anchor, hash).
- Citations: Each answer must include 2–4 citations; links resolve to the Docusaurus page + heading anchor.
- Scope control: Refuse off-topic or low-confidence questions with a standard “not covered” response and chapter suggestion when possible.
- Feedback: Thumbs up/down endpoint to store feedback with query, answer, chunk IDs, timestamps.

### Non-Functional
- Latency: P95 <= 2.5s end-to-end for average questions (excluding cold starts).
- Cost: Use small embeddings (e.g., MiniLM/bge-small) and streaming LLM responses.
- Security: Sanitize inputs, strip HTML/JS, detect prompt injection; do not leak secrets or PII.
- Observability: Log query, retrieval latency, chunk IDs, refusal reason, and feedback; no raw PII in logs.

### Out of Scope
- Multi-modal (images/video) handling.
- Long-term conversational memory beyond short-lived session context.
- Tool execution outside the RAG answer (e.g., running code).

## Technical Plan (high level)

- Backend: FastAPI service with endpoints `/chat`, `/feedback`, `/ingest`.
- Retrieval store: Qdrant collection for embeddings; metadata includes chapter, path, heading, anchor, hash.
- Metadata/feedback: Neon serverless Postgres for feedback, usage logs, ingestion run metadata.
- Embeddings: Small/CPU-friendly (e.g., `sentence-transformers/all-MiniLM-L6-v2` or `bge-small`).
- LLM: Configurable via env (e.g., GPT-4o-mini or Claude Haiku/Sonnet); prompts enforce scope and citations.
- Ingestion: Parse MD/MDX from `textbook/docs/**`, chunk with overlap, embed, upsert to Qdrant; store content hash/version tag.
- Frontend: Docusaurus chat widget that streams responses from `/chat`, displays citations with links to anchors, and a feedback control.

## Acceptance Criteria (minimum)

- Chat API returns grounded answers with citations or a refusal message; never hallucinates outside corpus.
- Citations link correctly to chapter anchors and are visible in the UI.
- Off-topic/prompt-injection attempts are refused and logged.
- Feedback posts to Postgres with query, answer, chunk IDs, and timestamp.
- Ingestion can be rerun without duplicates (idempotent upserts using content hash/IDs).
