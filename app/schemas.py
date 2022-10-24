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
    is_locked: bool
    published_at: int
    updated_at: int

    class Config():
        orm_mode = True


class PostingPreview(BaseModel):
    id: int
    title: str
    is_locked: bool

    class Config():
        orm_mode = True


class PostingCreate(BaseModel):
    title: str
    body: str
    is_locked: bool
    password: str

    class Config():
        orm_mode = True


class ShowCommunity(CommunityBase):
    id: int
    showname: str
    authority: Authority
    created_at: int
    published_at: int
    postings: List[PostingPreview]
    postings_count: int

    class Config():
        orm_mode = True


class UserCreate(BaseModel):
    nickname: str
    email: str
    password: str

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


class Comment(BaseModel):
    id: int
    user_id: int
    comment: str
    created_at: int
    post_id: int
    comment_class: int
    order: int
    group_id: int


class CommentCreate(BaseModel):
    comment: str
    group_id: int
