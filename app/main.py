from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import create_tables
from app.routers import auth, post, user


def create_app() -> FastAPI:
    """FastAPI 앱 생성"""
    # 앱 설정
    app_configs = {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs" if settings.SHOW_DOCS else None,
        "redoc_url": "/redoc" if settings.SHOW_DOCS else None,
    }

    # API 문서 표시 여부 설정
    if not settings.SHOW_DOCS:
        app_configs["openapi_url"] = None
        app_configs["docs_url"] = None
        app_configs["redoc_url"] = None

    app = FastAPI(**app_configs)

    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 개발용 - 프로덕션에서는 특정 도메인만 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 데이터베이스 테이블 생성
    create_tables()

    # 정적 파일 서빙 설정
    # 업로드된 파일들을 서빙하기 위해 추가
    os.makedirs("temp", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)

    app.mount("/temp", StaticFiles(directory="temp"), name="temp")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    # 라우터 등록
    # TODO: 라우터 파일들이 생성되면 여기에 추가
    # from app.routers import user, post
    app.include_router(auth.router, tags=["auth"])
    app.include_router(user.router, tags=["users"])
    app.include_router(post.router, tags=["posts"])
    app.include_router(post.list_router, tags=["posts"])

    return app


# 앱 인스턴스 생성
app = create_app()


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Welcome to CuteShrew Server",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
