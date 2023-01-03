from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.response.response_user_detail import ResponseUserDetail

from ..schemas import new_schemas

from .. import database
from ..repository import userRepo
from .oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/general', response_model=new_schemas.UserBase)
def create_user(request: new_schemas.UserCreate, db: Session = Depends(database.get_db)):
    return userRepo.create_user(request, db)


@router.post('/admin', response_model=new_schemas.UserBase)
def create_user_for_admin(request: new_schemas.UserCreate, db: Session = Depends(database.get_db), current_user: new_schemas.UserBase = Depends(get_current_user)):
    return userRepo.create_user_for_admin(request, db, current_user)


@router.get('/search', response_model=ResponseUserDetail)
def get_user(user_name: str, db: Session = Depends(database.get_db)):
    return userRepo.get_user(user_name, db)
