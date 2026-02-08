SHELL := /usr/bin/env bash

.PHONY: up down logs ps seed migrate revision fmt lint typecheck test
.PHONY: docs-serve docs-build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

migrate:
	docker compose exec api alembic upgrade head

revision:
	@if [ -z "$(m)" ]; then echo "Usage: make revision m='message'"; exit 1; fi
	docker compose exec api alembic revision --autogenerate -m "$(m)"

seed:
	docker compose exec api python -m diagnostics_lab.seed

fmt:
	python -m ruff format .

lint:
	python -m ruff check .

typecheck:
	python -m mypy diagnostics_lab

test:
	python -m pytest

docs-serve:
	pip install -r requirements-docs.txt
	mkdocs serve

docs-build:
	pip install -r requirements-docs.txt
	mkdocs build --strict
