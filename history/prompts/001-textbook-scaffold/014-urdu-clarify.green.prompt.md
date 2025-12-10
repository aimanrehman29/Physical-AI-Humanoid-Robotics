---
id: 014
title: Urdu clarify
stage: green
date: 2025-12-10
surface: agent
model: gpt-5
feature: 001-textbook-scaffold
branch: main
user: user
command: "/sp.clarify"
labels: [i18n, urdu, rtl]
links:
  spec: specs/001-textbook-scaffold/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - none
tests:
  - none
---

## Prompt

/sp.clarify  
Scope all chapters, formal Urdu style, dropdown toggle.

## Response snapshot

Confirmed: translate all chapters; use formal Urdu; use dropdown language switcher (Docusaurus i18n).

## Outcome

- ✅ Ambiguities resolved.
