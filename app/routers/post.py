from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, get_current_user_optional
from app.models.user import User
from app.schemas.post import (
    PostDetailRes,
    PostDraftRes,
    PostSummaryRes,
    PostUpdateReq,
    PostUpdateRes,
)
from app.services import post_service

# 메인 게시글 라우터
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

# 게시글 목록 관련 서브라우터
list_router = APIRouter(
    prefix="/list",
    tags=["posts"],
)


@router.get("/draft", response_model=PostDraftRes)
def get_draft_id(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return post_service.create_draft(db, current_user.id)


@router.put("/{post_id}", response_model=PostUpdateRes)
def update_post(
    post_id: str,
    post: PostUpdateReq,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return post_service.update_post(db, post_id, post, current_user.id)


@router.get("/{post_id}", response_model=PostDetailRes)
def get_post(
    post_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    # IP 주소 추출
    ip_address = None
    if "x-forwarded-for" in request.headers:
        ip_address = request.headers["x-forwarded-for"].split(",")[0].strip()
    elif "x-real-ip" in request.headers:
        ip_address = request.headers["x-real-ip"]
    else:
        ip_address = request.client.host if request.client else None

    # User Agent 추출
    user_agent = request.headers.get("user-agent")

    return post_service.get_post_detail(
        db=db,
        post_id=post_id,
        user_id=current_user.id if current_user else None,
        ip_address=ip_address,
        user_agent=user_agent,
    )


# 게시글 목록 관련 엔드포인트들
@list_router.get("/recent", response_model=List[PostSummaryRes])
def get_recent_posts(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
):
    return post_service.get_recent_posts(db, page, limit)


@list_router.get("/top", response_model=List[PostSummaryRes])
def get_top_posts(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
):
    return post_service.get_top_posts(db, page, limit)


# 서브라우터를 메인 라우터에 포함
router.include_router(list_router)
