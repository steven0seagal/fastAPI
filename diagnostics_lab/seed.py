from __future__ import annotations

from sqlalchemy import select

from diagnostics_lab.db.models.catalog import TestCatalogItem
from diagnostics_lab.db.models.user import User, UserRole
from diagnostics_lab.db.session import SessionLocal
from diagnostics_lab.security import hash_password
from diagnostics_lab.settings import get_settings

DEFAULT_CATALOG: list[dict[str, object]] = [
    {
        "code": "HGB",
        "name": "Hemoglobin",
        "unit": "g/dL",
        "specimen_type": "blood",
        "ref_low": 12.0,
        "ref_high": 17.5,
    },
    {
        "code": "WBC",
        "name": "White Blood Cells",
        "unit": "10^9/L",
        "specimen_type": "blood",
        "ref_low": 4.0,
        "ref_high": 11.0,
    },
    {
        "code": "GLU",
        "name": "Glucose (fasting)",
        "unit": "mg/dL",
        "specimen_type": "blood",
        "ref_low": 70.0,
        "ref_high": 99.0,
    },
]


def main() -> None:
    settings = get_settings()

    with SessionLocal() as db:
        admin = db.scalar(select(User).where(User.email == settings.default_admin_email))
        if not admin:
            admin = User(
                email=settings.default_admin_email,
                hashed_password=hash_password(settings.default_admin_password),
                full_name="Default Admin",
                role=UserRole.admin.value,
                is_active=True,
            )
            db.add(admin)

        for row in DEFAULT_CATALOG:
            existing = db.scalar(select(TestCatalogItem).where(TestCatalogItem.code == row["code"]))
            if existing:
                continue
            db.add(TestCatalogItem(**row))

        db.commit()

    print("Seed complete")


if __name__ == "__main__":
    main()
