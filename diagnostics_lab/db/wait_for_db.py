from __future__ import annotations

import time

from sqlalchemy import create_engine, text

from diagnostics_lab.settings import get_settings


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url, pool_pre_ping=True)

    deadline = time.time() + settings.db_wait_timeout_seconds
    last_err: Exception | None = None

    while time.time() < deadline:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"Waiting for database... ({type(e).__name__}: {e})")
            time.sleep(1)

    raise RuntimeError("Database did not become ready in time") from last_err


if __name__ == "__main__":
    main()
