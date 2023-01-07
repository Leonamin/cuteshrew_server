from typing import Optional
from pydantic import BaseModel, SecretStr


class RequestUserCreate(BaseModel):
    nickname: str
    email: str
    password: SecretStr

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
