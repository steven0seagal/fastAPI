import os
import sys
from pathlib import Path

# When running the `pytest` console script, Python's sys.path[0] is typically the
# virtualenv/bin directory, not the repo root. Add the repo root explicitly so
# `import diagnostics_lab` works regardless of how pytest is invoked.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# These must be set before importing the application modules (settings/DB/Celery).
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DEBUG", "0")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("CELERY_ALWAYS_EAGER", "1")
os.environ.setdefault("SECRET_KEY", "test-secret")
