from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PostDraftRes(BaseModel):
    id: str = Field(..., description="게시글 UUID")


class PostCreateReq(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="제목")
    content: str = Field(..., min_length=1, description="내용")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")


class PostUpdateReq(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="제목")
    content: Optional[str] = Field(None, min_length=1, description="내용")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")
    publish: Optional[bool] = Field(
        False, description="게시 여부"
    )


class PostUpdateRes(BaseModel):
    id: str = Field(..., description="게시글 ID")


class PostSummaryRes(BaseModel):
    id: str = Field(..., description="게시글 ID")
    title: str = Field(..., description="제목")
    short_content: str = Field(..., description="내용 요약")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")
    created_at: datetime = Field(..., description="생성일시")
    view_count: int = Field(..., description="조회수")
    like_count: int = Field(..., description="좋아요 수")
    comment_count: int = Field(..., description="댓글 수")
    writer_id: int = Field(..., description="작성자 ID")
    writer_name: str = Field(..., description="작성자 이름")
    writer_thumbnail_url: Optional[str] = Field(
        None, description="작성자 썸네일 이미지 URL"
    )


class PostDetailRes(BaseModel):
    id: str = Field(..., description="게시글 ID")
    title: str = Field(..., description="제목")
    content: str = Field(..., description="내용")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 URL")
    created_at: datetime = Field(..., description="생성일시")
    view_count: int = Field(..., description="조회수")
    like_count: int = Field(..., description="좋아요 수")
    comment_count: int = Field(..., description="댓글 수")
    writer_id: int = Field(..., description="작성자 ID")
    writer_name: str = Field(..., description="작성자 이름")
    writer_thumbnail_url: Optional[str] = Field(
        None, description="작성자 썸네일 이미지 URL"
    )


class PostLikeReq(BaseModel):
    post_id: str = Field(..., description="게시글 ID")


class PostLikeRes(BaseModel):
    id: str = Field(..., description="게시글 좋아요 ID")
