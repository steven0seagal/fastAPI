from __future__ import annotations

from diagnostics_lab.schemas.base import ORMModel


class Token(ORMModel):
    access_token: str
    token_type: str = "bearer"
