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
    
    # MySQL 설정 (향후 사용)
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "cuteshrew"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DATABASE: str = "cuteshrew"
    
    # 파일 저장소 설정
    STORAGE_TYPE: str = "local"  # local, s3
    STORAGE_BASE_PATH: str = "./uploads"
    STORAGE_TEMP_PATH: str = "./temp"
    STORAGE_POSTS_PATH: str = "./uploads/posts"
    
    # S3 설정 (향후 사용)
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET_NAME: str = "cuteshrew-uploads"
    S3_REGION: str = "ap-northeast-2"
    
    # 이미지 처리 설정
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    # API 문서 표시 여부 (true/false)
    SHOW_DOCS: bool = True

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
    
    @property
    def mysql_url(self) -> str:
        """MySQL 연결 URL 생성"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'


# 전역 설정 인스턴스
settings = Settings()
