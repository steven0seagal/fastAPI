from __future__ import annotations

from datetime import datetime

from pydantic import Field

from diagnostics_lab.schemas.base import ORMModel


class OrderCreate(ORMModel):
    patient_id: int
    test_codes: list[str] = Field(min_length=1, examples=[["HGB", "WBC"]])
    notes: str | None = None


class TestRequestRead(ORMModel):
    id: int
    status: str
    created_at: datetime
    resulted_at: datetime | None

    catalog_id: int


class OrderRead(ORMModel):
    id: int
    patient_id: int
    status: str
    notes: str | None
    ordered_at: datetime

    test_requests: list[TestRequestRead]
