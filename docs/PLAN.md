# Plan: FastAPI Diagnostics Lab Repository

## Goal

Build a single repository that demonstrates the most useful, production-relevant parts of FastAPI:

- API design and FastAPI features (routing, dependencies, OpenAPI, validation, error handling)
- Database integration (SQLAlchemy, migrations, transactions)
- Distributed background jobs (Celery + Redis)
- A ready-to-run Docker environment (API + DB + broker + workers)

The example domain is a **diagnostics laboratory** (patients, orders, samples, tests, results, QC).

## Audience

- Developers learning FastAPI beyond tutorials
- Teams who need a solid template for an internal lab/LIS-style service

## Scope (What This Repo Should Contain)

### FastAPI Feature Checklist

- App factory (`create_app`) and structured settings via env vars
- Routers per domain area and consistent tagging
- Dependency injection patterns
- Security patterns
  - OAuth2 password flow
  - JWT bearer tokens
  - Role-based authorization examples
- Request validation and response models (Pydantic v2)
- Pagination, filtering, sorting examples
- Consistent error responses (HTTPException + custom exceptions/handlers)
- Middleware examples
  - request-id/correlation-id
  - timing/logging
  - CORS
- Background work patterns
  - FastAPI `BackgroundTasks` (small in-process tasks)
  - Celery (reliable distributed tasks)
- Testing patterns
  - dependency overrides
  - DB isolation
  - auth helpers

### Database Checklist

- SQLAlchemy ORM models for core lab entities
- Alembic migrations
- Seed script for demo data
- Example patterns
  - transaction boundaries
  - idempotency and unique constraints
  - soft delete vs hard delete discussion

### Celery Checklist

- Celery worker and beat configuration
- Demonstration tasks
  - result enrichment (interpretation)
  - roll-up state transitions (order status)
  - periodic QC summary job
- Monitoring options
  - Flower profile

### Docker Checklist

- `docker-compose.yml` for development
- API container with an entrypoint that runs migrations
- Postgres + Redis healthchecks
- Separate services for API/worker/beat

## Roadmap

### Phase 1 (Baseline runnable template)

- FastAPI app with auth + lab domain routes
- Postgres models + migrations
- Celery tasks + docker compose
- Seed data and docs

Status: implemented (see `README.md`).

### Phase 2 (Diagnostics lab domain depth)

- Sample lifecycle
  - receive sample
  - reject sample with reason codes
- Results lifecycle
  - corrections/amendments
  - audit trail
- Turnaround time (TAT) metrics
  - ordered_at -> resulted_at
- Reference ranges
  - sex- and age-dependent ranges
  - unit normalization

### Phase 3 (FastAPI features expansion)

- File uploads
  - upload analyzer CSV
  - parse via Celery
- Streaming responses
  - stream generated report
- WebSockets
  - push order status updates to UI
- API versioning
  - `/v1` router prefix
- Rate limiting (optional)
- OpenAPI customization
  - tags metadata
  - security schemes docs

### Phase 4 (Operational hardening)

- Observability
  - structured logging fields
  - metrics endpoint (Prometheus)
  - tracing (OpenTelemetry)
- CI
  - ruff, mypy, pytest
- Security
  - password policy
  - secret rotation
  - least-privilege roles

## Definition Of Done

A new developer should be able to:

1. Clone the repo
2. `cp .env.example .env`
3. `docker compose up --build`
4. Seed data
5. Use Swagger to create a patient, place an order, submit results, and see Celery update statuses

And the docs should explain:

- Why each feature exists
- Where to find it in the code
- What to change first when adapting it to a real project
