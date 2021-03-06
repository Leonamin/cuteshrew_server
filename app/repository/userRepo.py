from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
from app.dependency import Authority

from app.hashing import Hash
from .. import models, schemas
import time


def create_user(request: schemas.UserCreate, db: Session):
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


def create_user_for_admin(request: schemas.User, db: Session, request_user: schemas.User):
    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not user.first().authority == (Authority.GOD or Authority.ADMIN or Authority.SUB_ADMIN):
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


def get_user(nickname: str, db: Session, request_user: schemas.User):
    request_user_info = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not request_user_info.first().nickname == nickname:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You can't check another user")

    user = db.query(models.User).filter(
        models.User.nickname == nickname).first()
    if not models.User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the name {nickname} not found")
    return user
