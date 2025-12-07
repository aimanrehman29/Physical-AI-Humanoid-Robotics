---
id: spec-kit-plus
title: Content Ops — Spec-Kit Plus Workflow
sidebar_position: 20
---

We use Spec-Kit Plus (already in `.specify/`) to keep the textbook consistent and reviewable.

## Authoring flow

1. **Capture intent**: Log user asks in Prompt History Records (PHRs) under `history/prompts/`.  
2. **Specs/plan/tasks**: Use the templates in `.specify/templates/` to outline what a chapter or feature needs.  
3. **Check prerequisites**:  
   ```powershell
   .specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
   ```  
   Ensures the current feature has `spec.md`, `plan.md`, and `tasks.md`.
4. **Write content**: Author MDX in `textbook/docs/`, following the shared template sections (objectives, key concepts, examples, checklist).  
5. **Validate**: Run `npm run build` for link checks; keep snippets runnable.  
6. **Record outcome**: Update tasks/checklists, and add a PHR summarizing the work.

## Style guardrails

- Use short headings, plain language, and runnable code (Python/JS).  
- Keep checklists actionable and close with “pitfalls to avoid.”  
- Prefer SVG/PNG images; diagrams can be generated via Mermaid or Draw.io exports.  
- Avoid hardcoding secrets; use `.env` patterns for examples.

## Where things live

- `.specify/`: Spec-Kit Plus templates and scripts.  
- `specs/<feature>/`: Spec/plan/tasks for each feature branch.  
- `history/prompts/<feature>/`: Prompt History Records.  
- `textbook/docs/`: Chapter content (MDX).
