from typing import List, Optional
from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

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
from app.config import settings

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


@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    post_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """이미지 업로드 API (로컬 테스트용)"""
    
    # 파일 타입 검증
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    # 파일 크기 검증 (10MB)
    if file.size and file.size > settings.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="파일 크기는 10MB를 초과할 수 없습니다.")
    
    # 파일 확장자 검증
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
    
    # 파일명 생성 (원본명 유지 + 중복 방지)
    original_name = Path(file.filename).stem
    extension = Path(file.filename).suffix
    unique_filename = f"{original_name}_{uuid.uuid4().hex[:8]}{extension}"
    
    # 업로드 경로 결정
    if post_id:
        # 게시글에 연결된 이미지: temp/{post_id}/
        upload_dir = Path(settings.STORAGE_TEMP_PATH) / post_id
    else:
        # 임시 이미지: temp/
        upload_dir = Path(settings.STORAGE_TEMP_PATH)
    
    # 디렉토리 생성
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일 저장
    file_path = upload_dir / unique_filename
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 저장 중 오류가 발생했습니다: {str(e)}")
    
    # 반환할 URL 생성
    if post_id:
        file_url = f"./temp/{post_id}/{unique_filename}"
    else:
        file_url = f"./temp/{unique_filename}"
    
    return {
        "success": True,
        "file_url": file_url,
        "filename": unique_filename,
        "original_name": file.filename,
        "size": len(content)
    }


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
