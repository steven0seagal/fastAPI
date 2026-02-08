import os

# These must be set before importing the application modules (settings/DB/Celery).
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DEBUG", "0")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("CELERY_ALWAYS_EAGER", "1")
os.environ.setdefault("SECRET_KEY", "test-secret")
