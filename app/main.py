from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config

from app.core.config import settings
from app.dependency import get_settings
from .models import models
from .database import engine
from .routers import api

from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


def get_application():
    app_configs = {"title" : settings.PROJECT_NAME, "version" : settings.VERSION}
    
    if settings.ENVIRONMENT not in settings.SHOW_DOCS_ENVIRONMENT:
        app_configs["openapi_url"] = None  

    _app = FastAPI(**app_configs)

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
    
    # _app.dependency_overrides[function_name] = override_function_name

    # _app.include_router(community.router)
    # _app.include_router(posting.router)
    # _app.include_router(user.router)
    # _app.include_router(authentication.router)
    # _app.include_router(comment.router)
    _app.include_router(api.router)

    return _app


app = get_application()

# @app.get("/info")
# def info(settings: config.Settings = Depends(get_settings)):
#     return settings

# 얘보다 뒤에 있으면 모든 /로 시작하는 응답이 안먹힌다.
@app.get("/")
async def index():
    return FileResponse('web/index.html', media_type='text/html')

app.mount("/", StaticFiles(directory="web"), name="web")

