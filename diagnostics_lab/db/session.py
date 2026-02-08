from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from diagnostics_lab.settings import get_settings

settings = get_settings()

engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
if settings.database_url.startswith("sqlite"):
    # Test-friendly defaults (FastAPI sync endpoints run in a threadpool).
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    if ":memory:" in settings.database_url:
        # Share a single in-memory DB across connections.
        engine_kwargs["poolclass"] = StaticPool

engine = create_engine(settings.database_url, **engine_kwargs)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
