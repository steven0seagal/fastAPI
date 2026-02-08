from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from diagnostics_lab.logging import configure_logging
from diagnostics_lab.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(debug=settings.debug)

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from diagnostics_lab.api.routes.auth import router as auth_router
    from diagnostics_lab.api.routes.catalog import router as catalog_router
    from diagnostics_lab.api.routes.health import router as health_router
    from diagnostics_lab.api.routes.orders import router as orders_router
    from diagnostics_lab.api.routes.patients import router as patients_router

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(patients_router)
    app.include_router(catalog_router)
    app.include_router(orders_router)

    return app


app = create_app()
