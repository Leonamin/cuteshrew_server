from typing import Optional
from pydantic import BaseModel, Field
from app.core.regex import email_regex


class UserCreateReq(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, description="이메일",
                       pattern=email_regex)
    password: str = Field(..., min_length=8,
                          max_length=100, description="비밀번호")
    name: str = Field(..., min_length=3, max_length=20, description="닉네임")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")
    description: Optional[str] = Field(None, description="설명")


class UserCreateRes(BaseModel):
    id: int = Field(..., description="유저 ID")


class UserLoginReq(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, description="이메일",
                       pattern=email_regex)
    password: str = Field(..., min_length=8,
                          max_length=100, description="비밀번호")


class UserLoginRes(BaseModel):
    access_token: str = Field(..., description="액세스 토큰")
    refresh_token: str = Field(..., description="리프레시 토큰")


class UserReadRes(BaseModel):
    id: int = Field(..., description="유저 ID")
    email: str = Field(..., min_length=5, max_length=255, description="이메일",
                       pattern=email_regex)
    name: str = Field(..., min_length=3, max_length=20, description="닉네임")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")


class UserProfileRes(BaseModel):
    id: int = Field(..., description="유저 프로필 ID")
    user_id: int = Field(..., description="유저 ID")
    name: str = Field(..., min_length=3, max_length=20, description="닉네임")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")
    description: Optional[str] = Field(None, description="설명")
    website_url: Optional[str] = Field(None, description="웹사이트 URL")
    instagram_url: Optional[str] = Field(None, description="인스타그램 URL")
    facebook_url: Optional[str] = Field(None, description="페이스북 URL")
