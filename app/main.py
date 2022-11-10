from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from . import models
from .database import engine
from .routers import api

from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    models.Base.metadata.create_all(bind=engine)

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

    # _app.include_router(community.router)
    # _app.include_router(posting.router)
    # _app.include_router(user.router)
    # _app.include_router(authentication.router)
    # _app.include_router(comment.router)
    _app.include_router(api.router)

    return _app


app = get_application()


@app.get("/")
async def index():
    return FileResponse('web/index.html', media_type='text/html')

app.mount("/", StaticFiles(directory="web"), name="web")
