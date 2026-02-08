#!/usr/bin/env bash
set -euo pipefail

python -m diagnostics_lab.db.wait_for_db
alembic upgrade head

exec "$@"
