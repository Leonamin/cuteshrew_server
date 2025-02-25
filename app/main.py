from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.initialize import create_db_metadata
from app.db.database import engine


def get_application():
    app_configs = {"title": settings.PROJECT_NAME, "version": settings.VERSION}

    if settings.ENVIRONMENT not in settings.SHOW_DOCS_ENVIRONMENT:
        app_configs["openapi_url"] = None

    _app = FastAPI(**app_configs)

    create_db_metadata(engine)

    _app.add_middleware(
        # FIXME allow origins 때문에 flutter에서 수신이 안됨 왜그러는지?
        # CORSMiddleware,
        # allow_origins=[str(origin)
        #                for origin in settings.BACKEND_CORS_ORIGINS],
        # allow_credentials=True,
        # allow_methods=["*"],
        # allow_headers=["*"],
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # _app.dependency_overrides[function_name] = override_function_name
    # _app.include_router(api_v2.router)

    return _app


app = get_application()
