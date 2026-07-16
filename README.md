# AI Voice Sales Manager

Professional monorepo foundation for a commercial AI Voice Sales Manager product.

## Stack

- Backend: Python 3.12, FastAPI, uv, async-ready architecture
- Frontend: Next.js, TypeScript, Tailwind CSS
- Infrastructure: Docker, Docker Compose
- Database: PostgreSQL
- Cache: Redis

## Repository structure

```text
voiceflow-ai/
├── apps/
│   ├── backend/
│   └── frontend/
├── packages/
├── infrastructure/
├── docker/
├── knowledge/
├── prompts/
├── docs/
│   ├── vision.md
│   ├── roadmap.md
│   ├── architecture.md
│   ├── decisions.md
│   └── dev-log.md
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Run with Docker Compose

```bash
docker compose up --build
```

Services:

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:8000>
- Health check: <http://localhost:8000/health>
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## Run backend locally

```bash
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload
```

The backend health check returns:

```json
{
  "status": "ok"
}
```

## Run frontend locally

```bash
cd apps/frontend
npm install
npm run dev
```

## Architectural decisions

- `apps/backend` and `apps/frontend` are independent applications so API and UI can be developed, deployed, and scaled separately.
- FastAPI request handlers are async-ready from the first endpoint, which fits future voice, telephony, CRM, and agent workflows.
- PostgreSQL and Redis are included in Docker Compose now because commercial sales workflows will need durable state and fast cache or queue-adjacent primitives.
- `packages` is reserved for shared contracts and SDK code once boundaries between applications become stable.
- `knowledge` and `prompts` are explicit top-level areas for future Knowledge Base and AI Agents work, but no AI logic is implemented yet.
- Documentation starts with vision, roadmap, architecture, decisions, and development log files to keep product and engineering context close to the code.
