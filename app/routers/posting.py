from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import postingRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/community/{name}",
    tags=['posting']
)


@router.get("")
def get_all(name: str, db: Session = Depends(database.get_db)):
    return postingRepo.get_all(name, db)


@router.get("/{id}", response_model=schemas.PostingResponse)
def get_post(name: str, id: int, password: Optional[str] = None, db: Session = Depends(database.get_db)):
    return postingRepo.get_post(name, id, password, db)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(name: str, request: schemas.PostingCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return postingRepo.create_post(name, request, db, current_user)

# update 할 때 .dict()로 형변환...


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(name: str, id: int, request: schemas.PostingCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return postingRepo.update_post(name, id, request, db, current_user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(name: str, id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return postingRepo.delete_post(name, id, db, current_user)
