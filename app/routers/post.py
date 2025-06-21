from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.post import (
    PostDetailRes,
    PostDraftRes,
    PostSummaryRes,
    PostUpdateReq,
    PostUpdateRes,
)
from app.services import post


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/draft", response_model=PostDraftRes)
def get_draft_id(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return post.create_draft(db, current_user.id)


@router.put("/{post_id}", response_model=PostUpdateRes)
def update_post(
    post_id: str,
    post: PostUpdateReq,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return post.update_post(db, post_id, post, current_user.id)


@router.get("/{post_id}", response_model=PostDetailRes)
def get_post(
    post_id: str,
    db: Session = Depends(get_db),
):
    return post.get_post_detail(db, post_id)


@router.get("/recent", response_model=List[PostSummaryRes])
def get_recent_posts(
    db: Session = Depends(get_db),
):
    pass


@router.get("/top", response_model=List[PostSummaryRes])
def get_top_posts(
    db: Session = Depends(get_db),
):
    pass
