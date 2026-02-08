from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from diagnostics_lab.db.models.base import Base


class TestCatalogItem(Base):
    __tablename__ = "test_catalog"
    __test__ = False  # prevent pytest from trying to collect this as a test class

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    specimen_type: Mapped[str | None] = mapped_column(String(64), nullable=True)

    ref_low: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    ref_high: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
