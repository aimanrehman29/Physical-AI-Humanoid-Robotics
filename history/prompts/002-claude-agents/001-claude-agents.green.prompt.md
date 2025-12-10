---
id: 001
title: Claude subagents and reusable skills
stage: green
date: 2025-12-10
surface: agent
model: gpt-5
feature: 002-claude-agents
branch: main
user: user
command: "/sp.implement (Claude agents)"
labels: [claude, agents, skills, backend, ui]
links:
  spec: history/prompts/001-textbook-scaffold/013-urdu-specification.green.prompt.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/agents.py
  - backend/app/main.py
  - backend/requirements.txt
  - textbook/src/components/ChatWidget/index.tsx
  - textbook/src/components/ChatWidget/agent-widget.module.css
tests:
  - not run (manual curl/npm start suggested)
---

## Prompt

/sp.implement — Start the implementation of Claude-powered intelligence (code explanations, agent skills, UI buttons).

## Response snapshot

Added Claude support in backend (`agents.py`, `/agent` endpoint) with code_explain/summary skills, Anthropic dependency, and UI “AI Tools” panel in the chat widget with an “Explain with Claude” button and code/question inputs.

## Outcome

- ✅ Backend: Claude client, code_explain/summary skills via `/agent`.
- ✅ Frontend: AI Tools panel in chat widget with code explain button.
- ⚠️ Next: wire chapter summary/quiz/QA skills, set ANTHROPIC_API_KEY/CLAUDE_MODEL, and test end-to-end.***
