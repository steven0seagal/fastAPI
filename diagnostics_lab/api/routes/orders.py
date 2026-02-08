from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from diagnostics_lab.api.deps import get_current_user
from diagnostics_lab.db.models.catalog import TestCatalogItem
from diagnostics_lab.db.models.order import LabOrder, OrderStatus, TestRequest, TestRequestStatus
from diagnostics_lab.db.models.patient import Patient
from diagnostics_lab.db.models.result import TestResult
from diagnostics_lab.db.models.sample import Sample
from diagnostics_lab.db.models.user import User
from diagnostics_lab.db.session import get_db
from diagnostics_lab.schemas.orders import OrderCreate, OrderRead
from diagnostics_lab.schemas.results import TestResultCreate, TestResultRead
from diagnostics_lab.schemas.samples import SampleCreate, SampleRead
from diagnostics_lab.tasks import process_result

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> LabOrder:
    patient = db.get(Patient, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown patient_id")

    codes = sorted({c.strip().upper() for c in payload.test_codes if c.strip()})
    if not codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="test_codes must not be empty"
        )

    items = list(db.scalars(select(TestCatalogItem).where(TestCatalogItem.code.in_(codes))).all())
    found = {i.code for i in items}
    missing = [c for c in codes if c not in found]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Unknown test codes", "missing": missing},
        )

    order = LabOrder(
        patient_id=payload.patient_id, status=OrderStatus.new.value, notes=payload.notes
    )
    for item in items:
        order.test_requests.append(
            TestRequest(catalog_id=item.id, status=TestRequestStatus.requested.value)
        )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> LabOrder:
    order = db.get(LabOrder, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("/{order_id}/samples", response_model=SampleRead, status_code=status.HTTP_201_CREATED)
def create_sample(
    order_id: int,
    payload: SampleCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> Sample:
    order = db.get(LabOrder, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    sample = Sample(
        order_id=order_id,
        barcode=payload.barcode,
        specimen_type=payload.specimen_type,
    )
    db.add(sample)
    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Barcode already exists"
        ) from err

    db.refresh(sample)
    return sample


@router.post(
    "/test-requests/{test_request_id}/result",
    response_model=TestResultRead,
    status_code=status.HTTP_201_CREATED,
)
def submit_result(
    test_request_id: int,
    payload: TestResultCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> TestResult:
    test_request = db.get(TestRequest, test_request_id)
    if not test_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test request not found")

    measured_at = payload.measured_at or datetime.now(UTC)

    result = TestResult(
        test_request_id=test_request_id,
        value=payload.value,
        unit=payload.unit,
        measured_at=measured_at,
    )

    test_request.status = TestRequestStatus.resulted.value
    test_request.resulted_at = measured_at

    order = db.get(LabOrder, test_request.order_id)
    if order and order.status == OrderStatus.new.value:
        order.status = OrderStatus.in_progress.value

    db.add(result)
    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Result already submitted"
        ) from err

    db.refresh(result)

    # Fan-out processing to Celery.
    process_result.delay(result.id)

    return result
