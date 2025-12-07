---
id: 009
title: Switch navbar logo to AVIF
stage: green
date: 2025-12-07
surface: agent
model: gpt-5
feature: 001-textbook-scaffold
branch: 001-textbook-scaffold
user: user
command: n/a
labels: [branding, bugfix]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - textbook/docusaurus.config.ts
  - textbook/src/components/HomepageFeatures/index.tsx
tests:
  - npm run build (textbook/)
---

## Prompt

logo.avif    
change with logo

## Response snapshot

Pointed the navbar logo to `logo.avif` and fixed the homepage feature card to render the PNG illustration as an image instead of as an SVG (which caused an SSG error). Build now passes.

## Outcome

- ✔ Impact: Navbar uses `logo.avif`; homepage feature image renders correctly.
- 🧪 Tests: `npm run build` (textbook/) passed.
- 📁 Files: Updated `docusaurus.config.ts` and `HomepageFeatures/index.tsx`.
- 🔜 Next prompts: None.
- 📝 Reflection: Non-SVG assets should render via `<img>` to avoid invalid SVG tag errors during static build.

## Evaluation notes (flywheel)

- Failure modes observed: SSG error due to PNG treated as SVG; resolved with conditional rendering.
- Graders run and results (PASS/FAIL): Not run.
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Consider WebP/AVIF for other hero assets if needed.
