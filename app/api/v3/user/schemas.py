from typing import Optional
from pydantic import BaseModel, Field, SecretStr


class RequestUserCreate(BaseModel):
    nickname: str = Field(min_length=1, max_length=20)
    email: str = Field(min_length=1, max_length=100)
    password: SecretStr = Field(min_length=1, max_length=20)

    class Config:
        schema_extra = {
            "example": {
                "nickname": "best_shrew",
                "email": "best_shrew@cuteshrew.xyz",
                "password": "password_what_you_want",
            }
        }


class ResponseUserPreview(BaseModel):
    nickname: str
    email: str

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "nickname": "best_shrew",
                "email": "best_shrew@cuteshrew.xyz",
            }
        }


class ResponseUserDetail(BaseModel):
    nickname: str
    email: str
    posting_count: Optional[int]
    comment_count: Optional[int]
    introduction: Optional[str]

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "nickname": "best_shrew",
                "email": "best_shrew@cuteshrew.xyz",
                "posting_count": 31,
                "comment_count": 5,
                "introduction": "let me tell you something... ACTUALLY I'M HAMSTER"
            }
        }
