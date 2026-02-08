# FastAPI Diagnostics Lab (Feature Repository)

A repository-style project that showcases "real" FastAPI patterns in a **diagnostics laboratory** domain:

- FastAPI routing, dependencies, validation (Pydantic), error handling, OpenAPI docs
- PostgreSQL integration via SQLAlchemy + Alembic migrations
- Async job processing via Celery + Redis (worker + beat)
- A ready-to-run Docker Compose environment (API + DB + broker + workers)

This is meant to be both:
1) a runnable starter, and
2) a curated set of examples you can copy into production services.

## Quickstart (Docker)

1. Create `.env` from the example:

```bash
cp .env.example .env
```

2. Start the stack:

```bash
docker compose up --build
```

3. Seed demo data (admin user + a small test catalog):

```bash
docker compose exec api python -m diagnostics_lab.seed
```

4. Open API docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Default Credentials (Dev)

After seeding:

- email: `admin@lab.local`
- password: `admin123`

Use `POST /auth/token` (OAuth2 password flow) to obtain a bearer token.

## What’s Implemented

- **Auth**: JWT bearer tokens (OAuth2 password flow)
- **Catalog**: minimal test catalog (e.g., HGB/WBC/GLU)
- **Patients**: CRUD basics
- **Orders**: create lab orders with test requests
- **Results**: submit a result for a test request
- **Celery**: result enrichment (interpretation) + order roll-up status
- **Health checks**: liveness/readiness endpoints

## Documentation

- `docs/PLAN.md` (roadmap + feature checklist)
- `docs/DOMAIN.md` (lab domain model + workflows)
- `docs/ARCHITECTURE.md` (module layout + patterns)
- `docs/RUNNING.md` (local vs Docker workflows)
- `docs/DB.md` (migrations + seeding)
- `docs/CELERY.md` (worker/beat tasks)
- `docs/CI_CD.md` (GitHub Actions CI/CD + releases)

## Repo Layout

- `diagnostics_lab/` application package
- `alembic/` migrations
- `docker-compose.yml` development stack
- `docker/entrypoint.sh` runs `alembic upgrade head` on container start

## Local Development (No Docker)

You can run it locally if you provide Postgres + Redis and set env vars accordingly:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

export DATABASE_URL='postgresql+psycopg://...'
export REDIS_URL='redis://...'
export SECRET_KEY='...'

uvicorn diagnostics_lab.main:app --reload
```

## Make Targets

- `make up` / `make down` / `make logs`
- `make seed`
- `make migrate`
- `make docs-serve` (MkDocs local preview)

## Repo Stats

As of 2026-02-07:

- Files (git-tracked + untracked, excluding ignored): 69
- Total lines (same scope): 2737
