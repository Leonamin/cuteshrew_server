from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import userRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/general', response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return userRepo.create_user(request, db)


@router.post('/admin', response_model=schemas.User)
def create_user_for_admin(request: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return userRepo.create_user_for_admin(request, db, current_user)


@router.get('/{name}', response_model=schemas.UserInformation)
def get_user(nickname: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return userRepo.get_user(nickname, db, current_user)
