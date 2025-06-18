from typing import List, Union, Optional
from pydantic import BaseModel, Field

from app.dependency import Authority

# 신 스키마


class PostingPreview(BaseModel):
    id: int
    title: str
    published_at: int
    updated_at: int
    user_id: Optional[int] = None
    is_locked: bool
    comment_count: Optional[int] = None

    class Config():
        orm_mode = True


class PostingBase(PostingPreview):
    body: Optional[str] = None
    password: Optional[str] = None

    class Config():
        orm_mode = True


class CommunityBase(BaseModel):
    id: Optional[int] = None
    name: str
    showname: str
    authority: Optional[Authority] = None
    created_at: Optional[int] = None
    published_at: Optional[int] = None
    posting_count: Optional[int] = None

    class Config():
        orm_mode = True


class UserPreview(BaseModel):
    nickname: str
    email: str

    class Config():
        orm_mode = True


class UserBase(UserPreview):
    id: Optional[int] = None

    created_at: Optional[int] = None
    authority: Optional[Authority] = None


class CommentBase(BaseModel):
    id: int
    user_id: int
    comment: str
    created_at: int
    post_id: int
    comment_class: Optional[int] = None
    order: Optional[int] = None
    group_id: Optional[int] = None

    class Config():
        orm_mode = True


class PostingCreate(BaseModel):
    title: str
    body: str
    is_locked: bool
    password: Optional[str] = None


class CommunityCreate(BaseModel):
    name: str
    showname: str
    authority: Authority


class UserCreate(BaseModel):
    nickname: str
    email: str
    password: str
    authority: Optional[Authority] = None


class CommentCreate(BaseModel):
    comment: str

# 응답


class ResponseShowCommunity(CommunityBase):
    postings: List[PostingBase]

    class Config():
        orm_mode = True


class ResponsePosting(PostingBase):
    creator: UserPreview
    own_community: CommunityBase


class ResponsePostingPreview(PostingPreview):
    creator: UserPreview
    own_community: CommunityBase


class ResponsePostingList(BaseModel):
    posting_count: int
    postings: List[ResponsePosting]


class ResponseComment(CommentBase):
    creator: UserPreview
    posting: Optional[ResponsePostingPreview] = None


class ResponseCommentList(BaseModel):
    comment_count: int
    comments: List[ResponseComment]

# 로그인


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
