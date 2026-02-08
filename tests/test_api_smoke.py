from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import select

from diagnostics_lab.db.models import Base
from diagnostics_lab.db.models.catalog import TestCatalogItem
from diagnostics_lab.db.models.user import User, UserRole
from diagnostics_lab.db.session import SessionLocal, engine, get_db
from diagnostics_lab.main import create_app
from diagnostics_lab.security import hash_password


def _bootstrap_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if not db.scalar(select(User).where(User.email == "admin@lab.local")):
            db.add(
                User(
                    email="admin@lab.local",
                    hashed_password=hash_password("admin123"),
                    role=UserRole.admin.value,
                    is_active=True,
                )
            )

        if not db.scalar(select(TestCatalogItem).where(TestCatalogItem.code == "HGB")):
            db.add(
                TestCatalogItem(
                    code="HGB",
                    name="Hemoglobin",
                    unit="g/dL",
                    specimen_type="blood",
                    ref_low=12.0,
                    ref_high=17.5,
                )
            )

        db.commit()


def test_smoke_flow() -> None:
    _bootstrap_db()

    app = create_app()

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    # Health
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    # Auth
    r = client.post("/auth/token", data={"username": "admin@lab.local", "password": "admin123"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create patient
    r = client.post(
        "/patients",
        headers=headers,
        json={"external_id": "MRN-1", "first_name": "Jan", "last_name": "Kowalski"},
    )
    assert r.status_code == 201
    patient_id = r.json()["id"]

    # Create order
    r = client.post(
        "/orders",
        headers=headers,
        json={"patient_id": patient_id, "test_codes": ["HGB"]},
    )
    assert r.status_code == 201
    order = r.json()
    assert order["status"] == "new"
    test_request_id = order["test_requests"][0]["id"]

    # Submit result (Celery eager mode will compute interpretation)
    r = client.post(
        f"/orders/test-requests/{test_request_id}/result",
        headers=headers,
        json={"value": 10.5, "unit": "g/dL"},
    )
    assert r.status_code == 201
    assert r.json()["interpretation"] in {"low", "normal", "high", "invalid", None}

    # Order should move to in_progress or completed (single test -> completed)
    r = client.get(f"/orders/{order['id']}", headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] in {"in_progress", "completed"}
