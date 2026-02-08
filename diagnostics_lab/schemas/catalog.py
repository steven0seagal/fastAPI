from __future__ import annotations

from datetime import datetime

from diagnostics_lab.schemas.base import ORMModel


class TestCatalogItemCreate(ORMModel):
    code: str
    name: str
    unit: str | None = None
    specimen_type: str | None = None
    ref_low: float | None = None
    ref_high: float | None = None


class TestCatalogItemRead(ORMModel):
    id: int
    code: str
    name: str
    unit: str | None
    specimen_type: str | None
    ref_low: float | None
    ref_high: float | None
    created_at: datetime
