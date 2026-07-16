# Decisions

## 2026-07-16: Start with a minimal monorepo

Use a small monorepo with separate backend and frontend applications. This keeps local development simple while leaving room for shared packages and infrastructure code.

## 2026-07-16: Keep AI logic out of the foundation

The initial implementation only includes platform scaffolding and a health endpoint. AI-specific behavior will be added after module contracts are defined.
