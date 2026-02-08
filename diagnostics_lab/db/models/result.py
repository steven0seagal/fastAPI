from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from diagnostics_lab.db.models.base import Base


class TestResult(Base):
    __tablename__ = "test_results"
    __test__ = False  # prevent pytest from trying to collect this as a test class

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_request_id: Mapped[int] = mapped_column(
        ForeignKey("test_requests.id", ondelete="CASCADE"), unique=True, index=True
    )

    value: Mapped[float | None] = mapped_column(Numeric(14, 4), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)

    interpretation: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
        doc="low|normal|high|invalid",
    )

    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    test_request = relationship("TestRequest", back_populates="result")
