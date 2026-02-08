from __future__ import annotations

from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from diagnostics_lab.db.session import get_db
from diagnostics_lab.settings import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))

    settings = get_settings()
    Redis.from_url(settings.redis_url).ping()
    return {"status": "ok"}
