from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

from app.hashing import Hash
from .. import models, schemas
import time


def create_user(request: schemas.User, db: Session):
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
    return user
