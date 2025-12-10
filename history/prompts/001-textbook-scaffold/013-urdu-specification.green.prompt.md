---
id: 013
title: Urdu support specification
stage: green
date: 2025-12-10
surface: agent
model: gpt-5
feature: 001-textbook-scaffold
branch: main
user: user
command: "/sp.specify"
labels: [i18n, urdu, rtl, spec]
links:
  spec: specs/001-textbook-scaffold/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - textbook/docusaurus.config.ts
tests:
  - none
---

## Prompt

/sp.specify  
Define the full specification for enabling Urdu translation (all chapters), RTL, dropdown toggle, embeddings that handle Urdu, free-tier optimized.

## Response snapshot

Outlined scope (all chapters), RTL/font requirements, Docusaurus i18n, use of multilingual embeddings, tagging Urdu docs in Qdrant, and maintaining matching slugs/IDs. Toggle via built-in language dropdown; optional preference persistence.

## Outcome

- ✅ Spec documented in response; no code changes in this step.
- ⚠️ Implementation tracked in subsequent steps.
