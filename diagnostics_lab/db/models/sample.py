from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from diagnostics_lab.db.models.base import Base


class SampleStatus(StrEnum):
    collected = "collected"
    received = "received"
    rejected = "rejected"


class Sample(Base):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("lab_orders.id", ondelete="CASCADE"), index=True
    )

    barcode: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    specimen_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=SampleStatus.collected.value)

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
