from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.response.response_user_detail import ResponseUserDetail
from ..models import models
from app.dependency import Authority

from app.hashing import Hash
from ..schemas import new_schemas
import time


def create_user(request: new_schemas.UserCreate, db: Session):
    new_user = models.User(
        nickname=request.nickname,
        email=request.email,
        password=Hash.bcrypt(request.password),
        authority=Authority.WRITER,
        created_at=int(time.time())
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_user_for_admin(request: new_schemas.UserBase, db: Session, request_user: new_schemas.UserBase):
    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not user.first().authority == (Authority.GOD or Authority.ADMIN or Authority.SUB_ADMIN):
        if user.first().authority < request.authority: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User has low authoriy {user.first().authority}")

    new_user = models.User(
        nickname=request.nickname,
        email=request.email,
        password=Hash.bcrypt(request.password),
        authority=request.authority,
        created_at=int(time.time())
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(nickname: str, db: Session):
    user = db.query(models.User).filter(
        models.User.nickname == nickname).first()
    if not models.User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the name {nickname} not found")
        
    # 게시글 개수 구하기
    posting_count = db.query(models.Posting)\
        .filter(
        models.Posting.user_id == user.id).count()
    
    # 댓글 개수 구하기
    comment_count = db.query(models.Comment)\
        .filter(
        models.Comment.user_id == user.id).count()
        
    introduction = "Not available now"

    response = ResponseUserDetail.from_orm(user)
    response.posting_count = posting_count
    response.comment_count = comment_count
    response.introduction = introduction
    
    return response
