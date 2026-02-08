from __future__ import annotations

from datetime import datetime

from diagnostics_lab.schemas.base import ORMModel


class TestResultCreate(ORMModel):
    value: float | None = None
    unit: str | None = None
    measured_at: datetime | None = None


class TestResultRead(ORMModel):
    id: int
    test_request_id: int
    value: float | None
    unit: str | None
    interpretation: str | None
    measured_at: datetime
    created_at: datetime
