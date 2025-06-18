from typing import List, Union
from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 기본 앱 설정
    PROJECT_NAME: str = "CuteShrew Server"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # CORS 설정
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # 보안 설정
    SECRET_KEY: str = Field(default="your-secret-key-here")

    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./cuteshrew.db"

    # API 문서 표시 여부 (true/false)
    SHOW_DOCS: bool = True

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'


# 전역 설정 인스턴스
settings = Settings()
