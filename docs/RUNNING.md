# Running The Project

## Docker (Recommended)

1. Create `.env`:

```bash
cp .env.example .env
```

2. Start services:

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

3. Seed demo data:

```bash
docker compose exec api python -m diagnostics_lab.seed
```

4. Optional: start Flower:

```bash
docker compose --profile flower up --build
```

Flower UI: `http://localhost:5555`

## Local (Without Docker)

Requirements:

- Postgres
- Redis

Then:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

export DATABASE_URL='postgresql+psycopg://user:pass@localhost:5432/diagnostics_lab'
export REDIS_URL='redis://localhost:6379/0'
export SECRET_KEY='change-me'

alembic upgrade head
python -m diagnostics_lab.seed
uvicorn diagnostics_lab.main:app --reload
```
