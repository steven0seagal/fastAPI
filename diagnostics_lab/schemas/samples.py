from __future__ import annotations

from datetime import datetime

from diagnostics_lab.schemas.base import ORMModel


class SampleCreate(ORMModel):
    barcode: str
    specimen_type: str | None = None


class SampleRead(ORMModel):
    id: int
    order_id: int
    barcode: str
    specimen_type: str | None
    status: str
    collected_at: datetime
    received_at: datetime | None
