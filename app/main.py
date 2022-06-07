from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from . import models
from .database import engine
from .routers import community, posting, authentication, user


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    models.Base.metadata.create_all(bind=engine)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(community.router)
    _app.include_router(posting.router)
    _app.include_router(user.router)
    _app.include_router(authentication.router)

    return _app


app = get_application()
