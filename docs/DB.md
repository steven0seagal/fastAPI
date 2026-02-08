# Database & Migrations

## ORM

SQLAlchemy ORM models live in:

- `diagnostics_lab/db/models/`

## Alembic

- Config: `alembic.ini`
- Environment: `alembic/env.py`
- Migrations: `alembic/versions/`

The Docker entrypoint runs:

- `alembic upgrade head`

on container startup.

## Creating A New Migration

After changing models:

```bash
docker compose exec api alembic revision --autogenerate -m "your message"
docker compose exec api alembic upgrade head
```

## Seed Data

Demo data is created by:

```bash
docker compose exec api python -m diagnostics_lab.seed
```

This creates:

- a default admin user
- a small test catalog (HGB/WBC/GLU)
