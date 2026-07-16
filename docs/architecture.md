# Architecture

The repository is organized as a monorepo with independently runnable applications and shared extension points.

## Applications

- `apps/backend`: Python 3.12 FastAPI service with async-ready request handlers.
- `apps/frontend`: Next.js TypeScript application with Tailwind CSS.

## Platform Directories

- `packages`: future shared libraries, SDKs, and typed contracts.
- `infrastructure`: deployment and provisioning definitions.
- `docker`: Docker-related helper files that are not app-specific.
- `knowledge`: future source materials and fixtures for Knowledge Base work.
- `prompts`: future prompt templates and agent instructions.
- `docs`: product and engineering documentation.

## Future Module Boundaries

The foundation leaves clear seams for Voice Engine, CRM, Telephony, Knowledge Base, and AI Agents without implementing AI logic prematurely.
