# Architecture

## High-Level

- **FastAPI** handles HTTP requests and validates payloads.
- **SQLAlchemy** persists state in Postgres.
- **Celery** processes background jobs reliably (separate worker process).
- **Redis** acts as the Celery broker/result backend.

## Module Layout

- `diagnostics_lab/main.py`
  - app factory (`create_app`) + router wiring
- `diagnostics_lab/settings.py`
  - typed settings loaded from env (`.env` supported)
- `diagnostics_lab/db/`
  - `session.py` engine + session factory
  - `models/` ORM models
- `diagnostics_lab/api/`
  - `deps.py` shared dependencies (db session, current user, role checks)
  - `routes/` API routers grouped by domain
- `diagnostics_lab/celery_app.py`
  - Celery app configuration + beat schedule
- `diagnostics_lab/tasks.py`
  - asynchronous processing (result interpretation, order roll-up)

## Patterns Used

### Dependency Injection

- DB session: `Depends(get_db)`
- Auth: `Depends(get_current_user)`
- Role checks: `Depends(require_role("admin"))`

### "Write fast, enrich later" with Celery

- API endpoints persist the minimal data quickly.
- Celery tasks perform:
  - derived fields (interpretation)
  - cross-entity rollups (order status)

This prevents long-running requests and isolates background work.
