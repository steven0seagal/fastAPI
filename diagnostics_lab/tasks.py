from __future__ import annotations

from datetime import UTC, datetime, timedelta

import structlog
from sqlalchemy import select

from diagnostics_lab.celery_app import celery_app
from diagnostics_lab.db.models.order import LabOrder, OrderStatus, TestRequest, TestRequestStatus
from diagnostics_lab.db.models.result import TestResult
from diagnostics_lab.db.session import SessionLocal

log = structlog.get_logger(__name__)


@celery_app.task(name="diagnostics_lab.tasks.process_result")
def process_result(result_id: int) -> None:
    """Compute interpretation and roll-up status to the lab order.

    This demonstrates a typical pattern:
    1) API persists the raw result quickly.
    2) Celery does enrichment + state transitions.
    """

    with SessionLocal() as db:
        result = db.get(TestResult, result_id)
        if not result:
            log.warning("result_not_found", result_id=result_id)
            return

        test_request = db.get(TestRequest, result.test_request_id)
        if not test_request:
            log.warning("test_request_not_found", test_request_id=result.test_request_id)
            return

        # Interpret numeric result if reference range is defined.
        # catalog_item is joined on access (relationship lazy="joined").
        item = test_request.catalog_item
        if result.value is None:
            result.interpretation = "invalid"
        elif item and (item.ref_low is not None) and (item.ref_high is not None):
            if float(result.value) < float(item.ref_low):
                result.interpretation = "low"
            elif float(result.value) > float(item.ref_high):
                result.interpretation = "high"
            else:
                result.interpretation = "normal"

        # Update order status if not cancelled.
        order = db.get(LabOrder, test_request.order_id)
        if order and order.status != OrderStatus.cancelled.value:
            stmt = select(TestRequest.status).where(TestRequest.order_id == order.id)
            statuses = list(db.scalars(stmt).all())
            non_cancelled = [s for s in statuses if s != TestRequestStatus.cancelled.value]
            if non_cancelled and all(s == TestRequestStatus.resulted.value for s in non_cancelled):
                order.status = OrderStatus.completed.value
            else:
                order.status = OrderStatus.in_progress.value

        db.commit()


@celery_app.task(name="diagnostics_lab.tasks.daily_qc_summary")
def daily_qc_summary() -> None:
    """Example periodic task (Celery Beat).

    In a real lab you might aggregate QC results, analyzer error rates, TAT metrics, etc.
    """

    since = datetime.now(UTC) - timedelta(days=1)

    with SessionLocal() as db:
        stmt = (
            select(LabOrder)
            .where(LabOrder.status == OrderStatus.completed.value)
            .where(LabOrder.ordered_at >= since)
        )
        completed_last_24h = len(list(db.scalars(stmt).all()))

    log.info("qc_summary", completed_last_24h=completed_last_24h)
