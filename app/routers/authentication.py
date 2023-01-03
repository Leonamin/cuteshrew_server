from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import time

from ..schemas import schemas

from ..models import models
from .. import database, token
from ..hashing import Hash

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

ACCESS_TOKEN_EXPIRE_WEEK = 1

"""
expires_time: 토큰 만료 시간 UnixTimeStamp 초단위
"""
@router.post('')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.nickname == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invaild Credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    expires_delta = timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEK)
    access_token, expire_time = token.create_access_token(data={"sub": user.email}, expires_delta=expires_delta)
    expire_time = round(time.mktime(expire_time.timetuple()))
    
    return {"access_token": access_token, "token_type": "bearer", "expire_time": expire_time}
