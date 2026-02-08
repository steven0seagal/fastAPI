"""init

Revision ID: 0001_init
Revises:
Create Date: 2026-02-07

"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="lab_tech"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("sex", sa.String(length=16), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("external_id", name="uq_patients_external_id"),
    )
    op.create_index("ix_patients_external_id", "patients", ["external_id"], unique=True)

    op.create_table(
        "test_catalog",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("unit", sa.String(length=32), nullable=True),
        sa.Column("specimen_type", sa.String(length=64), nullable=True),
        sa.Column("ref_low", sa.Numeric(12, 4), nullable=True),
        sa.Column("ref_high", sa.Numeric(12, 4), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("code", name="uq_test_catalog_code"),
    )
    op.create_index("ix_test_catalog_code", "test_catalog", ["code"], unique=True)

    op.create_table(
        "lab_orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="new"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("ordered_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_lab_orders_patient_id", "lab_orders", ["patient_id"], unique=False)
    op.create_index("ix_lab_orders_status", "lab_orders", ["status"], unique=False)

    op.create_table(
        "samples",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("barcode", sa.String(length=64), nullable=False),
        sa.Column("specimen_type", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="collected"),
        sa.Column("collected_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["lab_orders.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("barcode", name="uq_samples_barcode"),
    )
    op.create_index("ix_samples_order_id", "samples", ["order_id"], unique=False)
    op.create_index("ix_samples_barcode", "samples", ["barcode"], unique=True)

    op.create_table(
        "test_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("catalog_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="requested"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("resulted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["lab_orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["catalog_id"], ["test_catalog.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_test_requests_order_id", "test_requests", ["order_id"], unique=False)
    op.create_index("ix_test_requests_catalog_id", "test_requests", ["catalog_id"], unique=False)
    op.create_index("ix_test_requests_status", "test_requests", ["status"], unique=False)

    op.create_table(
        "test_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_request_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.Numeric(14, 4), nullable=True),
        sa.Column("unit", sa.String(length=32), nullable=True),
        sa.Column("interpretation", sa.String(length=16), nullable=True),
        sa.Column("measured_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["test_request_id"], ["test_requests.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("test_request_id", name="uq_test_results_test_request_id"),
    )
    op.create_index(
        "ix_test_results_test_request_id", "test_results", ["test_request_id"], unique=True
    )


def downgrade() -> None:
    op.drop_index("ix_test_results_test_request_id", table_name="test_results")
    op.drop_table("test_results")

    op.drop_index("ix_test_requests_status", table_name="test_requests")
    op.drop_index("ix_test_requests_catalog_id", table_name="test_requests")
    op.drop_index("ix_test_requests_order_id", table_name="test_requests")
    op.drop_table("test_requests")

    op.drop_index("ix_samples_barcode", table_name="samples")
    op.drop_index("ix_samples_order_id", table_name="samples")
    op.drop_table("samples")

    op.drop_index("ix_lab_orders_status", table_name="lab_orders")
    op.drop_index("ix_lab_orders_patient_id", table_name="lab_orders")
    op.drop_table("lab_orders")

    op.drop_index("ix_test_catalog_code", table_name="test_catalog")
    op.drop_table("test_catalog")

    op.drop_index("ix_patients_external_id", table_name="patients")
    op.drop_table("patients")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
