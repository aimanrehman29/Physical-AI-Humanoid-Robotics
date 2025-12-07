# Humanoid Robotics Textbook

This Docusaurus v3 site hosts the Humanoid Robotics & Physical AI textbook. Content is authored in MDX, with Spec-Kit Plus used for specs, plans, and prompt history tracking.

## Setup

```bash
npm install
```

## Local development

```bash
npm run start
```

The dev server runs at http://localhost:3000/ with hot reload.

## Build

```bash
npm run build
```

## Spec-Kit Plus checks

Run prerequisite checks for the active feature (expects `specs/<feature>/plan.md` and `tasks.md`):

```bash
npm run content:spec-check
```

## Deploy

Configure your hosting target (e.g., GitHub Pages) and run:

```bash
npm run deploy
```
