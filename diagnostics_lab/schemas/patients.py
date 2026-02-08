from __future__ import annotations

from datetime import date, datetime

from pydantic import Field

from diagnostics_lab.schemas.base import ORMModel


class PatientCreate(ORMModel):
    external_id: str | None = Field(default=None, examples=["MRN-000123"])
    first_name: str
    last_name: str
    dob: date | None = None
    sex: str | None = Field(default=None, examples=["female", "male"])


class PatientUpdate(ORMModel):
    external_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    dob: date | None = None
    sex: str | None = None


class PatientRead(ORMModel):
    id: int
    external_id: str | None
    first_name: str
    last_name: str
    dob: date | None
    sex: str | None
    created_at: datetime
