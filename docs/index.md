# FastAPI Diagnostics Lab

This repo is a runnable, copy-paste friendly reference project focused on the **diagnostics laboratory** domain.

It demonstrates:

- FastAPI: routers, dependencies, OpenAPI docs, validation, auth
- Database: PostgreSQL + SQLAlchemy + Alembic migrations
- Background jobs: Celery + Redis (worker + beat)
- Docker: full local environment via Docker Compose

## Start Here

- Quickstart: `docs/RUNNING.md`
- API demo flow: `docs/API.md`
- Roadmap/checklist: `docs/PLAN.md`

## Local Dev Commands

```bash
cp .env.example .env

docker compose up --build

docker compose exec api python -m diagnostics_lab.seed
```

API docs: `http://localhost:8000/docs`
