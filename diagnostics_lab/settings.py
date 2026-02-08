from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Diagnostics Lab API"
    app_env: str = Field(default="dev", description="dev|test|prod")
    debug: bool = False

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/diagnostics_lab"
    redis_url: str = "redis://localhost:6379/0"

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None
    celery_always_eager: bool = False

    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60

    default_admin_email: str = "admin@lab.local"
    default_admin_password: str = "admin123"

    db_wait_timeout_seconds: int = 30

    cors_allow_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if not s.celery_broker_url:
        s.celery_broker_url = s.redis_url
    if not s.celery_result_backend:
        # Default to a different Redis DB index than the broker.
        # Example: redis://host:6379/0 -> redis://host:6379/1
        base, _, db = s.redis_url.rpartition("/")
        if base and db.isdigit():
            s.celery_result_backend = f"{base}/{int(db) + 1}"
        else:
            s.celery_result_backend = s.redis_url
    return s
