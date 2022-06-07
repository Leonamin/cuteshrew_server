from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import userRepo

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/', response_model=schemas.User)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return userRepo.create_user(request, db)


@router.get('/{name}', response_model=schemas.UserInformation)
def create_user(nickname: str, db: Session = Depends(database.get_db)):
    return userRepo.get_user(nickname, db)
