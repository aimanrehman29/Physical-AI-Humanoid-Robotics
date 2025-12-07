---
id: 002
title: Fix chunk load error
stage: green
date: 2025-12-07
surface: agent
model: gpt-5
feature: 001-textbook-scaffold
branch: 001-textbook-scaffold
user: user
command: n/a
labels: [bugfix, docusaurus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - none (cache clean only)
tests:
  - npm run clear (textbook/)
  - npm run build (textbook/)
---

## Prompt

ERROR
Unexpected token '<'
SyntaxError: Unexpected token '<'
ERROR
Loading chunk 5c868d36 failed.
(missing: http://localhost:3000/5c868d36.js)
ChunkLoadError
    at __webpack_require__.f.j (http://localhost:3000/runtime~main.js:803:29)
    at http://localhost:3000/runtime~main.js:146:40
    at Array.reduce (<anonymous>)
    at __webpack_require__.e (http://localhost:3000/runtime~main.js:145:67)
    at fn.e (http://localhost:3000/runtime~main.js:341:50)
    at __WEBPACK_DEFAULT_EXPORT__.5c868d36 (webpack-internal:///./.docusaurus/registry.js:5:9160)
    at load (webpack-internal:///./node_modules/react-loadable/lib/index.js:28:17)
    at eval (webpack-internal:///./node_modules/react-loadable/lib/index.js:56:20)
    at Array.forEach (<anonymous>)
    at loadMap (webpack-internal:///./node_modules/react-loadable/lib/index.js:55:22)

## Response snapshot

Cleared Docusaurus caches/build (`npm run clear`) and rebuilt the site (`npm run build`) to regenerate hashed chunks; build now succeeds without missing chunk errors.

## Outcome

- ✔ Impact: Regenerated bundles; missing chunk issue resolved after cache clear + rebuild.
- 🧪 Tests: `npm run clear`, `npm run build` (textbook/) passed.
- 📁 Files: No tracked files changed (only regenerated build/cache).
- 🔜 Next prompts: Run `npm run serve` and hard-refresh browser if any cache persists.
- 📝 Reflection: Chunk-load errors often come from stale bundles; clear `.docusaurus`/`build` when hashes change.

## Evaluation notes (flywheel)

- Failure modes observed: Stale bundle reference causing 404 and HTML fallback.
- Graders run and results (PASS/FAIL): Not run.
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): If errors persist, clear browser cache or disable service worker and retry.
