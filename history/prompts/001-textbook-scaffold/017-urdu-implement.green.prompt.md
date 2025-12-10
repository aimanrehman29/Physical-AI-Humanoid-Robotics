---
id: 017
title: Urdu implementation
stage: green
date: 2025-12-10
surface: agent
model: gpt-5
feature: 001-textbook-scaffold
branch: main
user: user
command: "/sp.implement"
labels: [i18n, urdu, rtl, implementation]
links:
  spec: specs/001-textbook-scaffold/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - textbook/docusaurus.config.ts
  - textbook/src/theme/Root.tsx
  - textbook/src/css/custom.css
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/01-foundations.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/02-humanoid-basics.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/03-ros2-fundamentals.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/04-digital-twin.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/05-vision-language-action.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/chapters/06-productization.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/intro.md
  - textbook/i18n/ur/docusaurus-plugin-content-docs/current/content-ops/spec-kit-plus.md
tests:
  - npm run build
---

## Prompt

/sp.implement  
Start the code implementation for Urdu: bilingual setup, RTL, translations, toggle, deploy.

## Response snapshot

Implemented Urdu locale, RTL and font styling, language dropdown, Urdu homepage and all chapters, and Urdu Content Ops page. Fixed YAML/frontmatter issues and ensured Urdu build passes.

## Outcome

- ✅ Urdu i18n live with all chapters/homepage/content ops translated.
- ✅ RTL styling via Root hook and CSS; code blocks remain LTR.
- ✅ Build succeeds for en/ur (`npm run build`).
- ⚠️ Next: ingest Urdu docs into Qdrant with lang tags and verify Urdu answers/citations.
