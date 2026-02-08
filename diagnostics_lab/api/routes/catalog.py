from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from diagnostics_lab.api.deps import get_current_user, require_role
from diagnostics_lab.db.models.catalog import TestCatalogItem
from diagnostics_lab.db.models.user import User
from diagnostics_lab.db.session import get_db
from diagnostics_lab.schemas.catalog import TestCatalogItemCreate, TestCatalogItemRead

router = APIRouter(prefix="/catalog/tests", tags=["catalog"])


@router.get("", response_model=list[TestCatalogItemRead])
def list_tests(
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> list[TestCatalogItem]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)

    stmt = select(TestCatalogItem).order_by(TestCatalogItem.code.asc()).limit(limit).offset(offset)
    if q:
        like = f"%{q.strip()}%"
        stmt = (
            select(TestCatalogItem)
            .where((TestCatalogItem.code.ilike(like)) | (TestCatalogItem.name.ilike(like)))
            .order_by(TestCatalogItem.code.asc())
            .limit(limit)
            .offset(offset)
        )
    return list(db.scalars(stmt).all())


@router.post("", response_model=TestCatalogItemRead, status_code=status.HTTP_201_CREATED)
def create_test(
    payload: TestCatalogItemCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role("admin")),
) -> TestCatalogItem:
    item = TestCatalogItem(
        code=payload.code,
        name=payload.name,
        unit=payload.unit,
        specimen_type=payload.specimen_type,
        ref_low=payload.ref_low,
        ref_high=payload.ref_high,
    )
    db.add(item)
    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Test code already exists"
        ) from err

    db.refresh(item)
    return item
