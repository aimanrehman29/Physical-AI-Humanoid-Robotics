---
id: 012
title: Urdu configuration
stage: green
date: 2025-12-10
surface: agent
model: gpt-5
feature: 001-textbook-scaffold
branch: main
user: user
command: "/sp.configuration"
labels: [i18n, urdu, rtl]
links:
  spec: specs/001-textbook-scaffold/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - textbook/docusaurus.config.ts
  - textbook/src/css/custom.css
  - textbook/src/theme/Root.tsx
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/01-foundations.md
tests:
  - npm run build
---

## Prompt

/sp.configuration  
Enable Urdu language support within the Physical AI & Humanoid Robotics textbook. Scope: all chapters; RTL support; toggle between English/Urdu.

## Response snapshot

Enabled Docusaurus i18n with Urdu locale, added RTL toggle hooks and Urdu font stack, and created an Urdu version of Chapter 1. Language dropdown added to navbar; RTL styling applies on Urdu locale.

## Outcome

- ✅ i18n and RTL wiring in place with Urdu locale and dropdown.
- ✅ Urdu Chapter 1 stub created.
- ⚠️ Remaining chapters still to translate and ingest.
- Tests: `npm run build` (after fixes).
