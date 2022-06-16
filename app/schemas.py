from typing import List, Union
from pydantic import BaseModel, Field

from app.dependency import Authority


class CommunityBase(BaseModel):
    name: str
    showname: str
    authority: Authority

    class Config():
        orm_mode = True


class PostingBase(BaseModel):
    id: int
    title: str
    body: str

    class Config():
        orm_mode = True


class PostingPreview(BaseModel):
    id: int
    title: str

    class Config():
        orm_mode = True


class PostingCreate(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class ShowCommunity(CommunityBase):
    id: int
    showname: str
    authority: Authority
    created_at = int
    published_at = int
    postings: List[PostingPreview]

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
