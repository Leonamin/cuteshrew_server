from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.post import PostCreateReq, PostCreateRes, PostDetailRes, PostSummaryRes, PostUpdateReq, PostUpdateRes


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post("/", response_model=PostCreateRes)
def create_post(
    post: PostCreateReq,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pass


@router.get("/{post_id}", response_model=PostDetailRes)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    pass


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


@router.put("/{post_id}", response_model=PostUpdateRes)
def update_post(
    post_id: int,
    post: PostUpdateReq,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pass
