---
id: 001
title: RAG chatbot constitution
stage: green
date: 2025-12-07
surface: agent
model: gpt-5
feature: none
branch: main
user: user
command: n/a
labels: [constitution, rag]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

Define the overall structure and purpose of the RAG chatbot integration for the Physical AI & Humanoid Robotics textbook. This chatbot will use the textbook's content to answer user questions based on the chapters in the book."

Example:

Purpose: Create a Retrieval-Augmented Generation (RAG) chatbot to answer questions related to the Physical AI & Humanoid Robotics textbook.

Scope:

Use FastAPI to create the backend for the chatbot.

Integrate RAG with Qdrant and Neon Serverless Postgres for dynamic retrieval of content.

The chatbot will answer only based on the content in the textbook.

The chatbot will be embedded in the Docusaurus website.

## Response snapshot

Added the RAG chatbot constitution with scope, safety, retrieval-first, and architecture constraints (FastAPI + Qdrant + Neon) in `.specify/memory/constitution.md`.

## Outcome

- ✔ Impact: Charter for RAG chatbot captured in the constitution.
- 🧪 Tests: none.
- 📁 Files: `.specify/memory/constitution.md`.
- 🔜 Next prompts: plan/tasks already defined; next is implementation.
- 📝 Reflection: This sets governance and guardrails; implementation still pending.

## Evaluation notes (flywheel)

- Failure modes observed: none.
- Graders run and results (PASS/FAIL): not run.
- Next experiment: implement ingestion + retrieval pipeline.
