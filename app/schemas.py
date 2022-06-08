from enum import Enum
from typing import List, Union
from pydantic import BaseModel

from app.dependency import Authority


class CommunityBase(BaseModel):
    name: str
    showname: str
    type: int

    class Config():
        orm_mode = True


class PostingBase(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class ShowCommunity(CommunityBase):
    showname: str
    type: int
    created_at = int
    published_at = int
    postings: List[PostingBase]

    class Config():
        orm_mode = True


class User(BaseModel):
    nickname: str
    email: str
    password: str

    authority: Authority

    class Config():
        orm_mode = True


class UserInformation(BaseModel):
    nickname: str
    email: str
    password: str

    authority: Authority
    created_at: int

    postings: List[PostingBase]

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
