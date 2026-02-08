# Celery

## Why Celery Here?

Diagnostics lab workflows often require work that should not block the HTTP request:

- result enrichment (flags/interpretation)
- report generation
- sending notifications
- periodic QC summaries

Celery demonstrates reliable background processing with a separate worker process.

## Configuration

Settings are read from env (see `.env.example`):

- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `CELERY_ALWAYS_EAGER` (useful for tests/local experiments)

Implementation:

- `diagnostics_lab/celery_app.py`

## Tasks

Implemented tasks:

- `diagnostics_lab.tasks.process_result(result_id)`
  - computes `TestResult.interpretation`
  - updates `LabOrder.status` (roll-up)

- `diagnostics_lab.tasks.daily_qc_summary()`
  - periodic example task configured via Celery Beat

## Running

With Docker Compose:

- worker: `worker` service
- beat: `beat` service

Optional monitoring:

- `docker compose --profile flower up --build`
