from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from diagnostics_lab.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "diagnostics_lab",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["diagnostics_lab.tasks"],
)

celery_app.conf.update(
    task_always_eager=settings.celery_always_eager,
    task_eager_propagates=True,
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "daily-qc-summary": {
        "task": "diagnostics_lab.tasks.daily_qc_summary",
        "schedule": crontab(minute=0, hour=2),
    }
}
