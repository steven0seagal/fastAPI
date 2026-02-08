# Testing

This repo uses pytest.

## Running

```bash
pip install -r requirements-dev.txt
pytest
```

## Patterns Demonstrated

- dependency overrides (DB session)
- test-friendly settings (SQLite + Celery eager mode)
