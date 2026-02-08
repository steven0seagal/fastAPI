from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from diagnostics_lab.db.models.base import Base


class OrderStatus(StrEnum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class TestRequestStatus(StrEnum):
    requested = "requested"
    resulted = "resulted"
    cancelled = "cancelled"


class LabOrder(Base):
    __tablename__ = "lab_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="RESTRICT"), index=True
    )

    status: Mapped[str] = mapped_column(String(32), default=OrderStatus.new.value, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    ordered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    test_requests: Mapped[list[TestRequest]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    samples = relationship(
        "Sample",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class TestRequest(Base):
    __tablename__ = "test_requests"
    __test__ = False  # prevent pytest from trying to collect this as a test class

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("lab_orders.id", ondelete="CASCADE"), index=True
    )
    catalog_id: Mapped[int] = mapped_column(
        ForeignKey("test_catalog.id", ondelete="RESTRICT"), index=True
    )

    status: Mapped[str] = mapped_column(
        String(32), default=TestRequestStatus.requested.value, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resulted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    order: Mapped[LabOrder] = relationship(back_populates="test_requests")
    catalog_item = relationship("TestCatalogItem", lazy="joined")
    result = relationship(
        "TestResult", back_populates="test_request", uselist=False, lazy="selectin"
    )
