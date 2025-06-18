from pydantic import BaseModel, Field
from typing import Optional
from app.core.regex import email_regex


class AuthSignUpReq(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, description="이메일",
                       pattern=email_regex)
    password: str = Field(..., min_length=8,
                          max_length=100, description="비밀번호")
    name: str = Field(..., min_length=3, max_length=20, description="닉네임")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")
    description: Optional[str] = Field(None, description="설명")


class AuthSignUpRes(BaseModel):
    id: int = Field(..., description="유저 ID")


class AuthSignInReq(BaseModel):
    user_id: str = Field(..., min_length=5, max_length=255, description="이메일")
    password: str = Field(..., min_length=8,
                          max_length=100, description="비밀번호")


class AuthSignInRes(BaseModel):
    access_token: str = Field(..., description="액세스 토큰")
    refresh_token: str = Field(..., description="리프레시 토큰")
