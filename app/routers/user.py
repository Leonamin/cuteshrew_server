from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreateReq, UserCreateRes, UserLoginReq, UserLoginRes
from app.services import auth

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/signup", response_model=UserCreateRes)
def create_user(user: UserCreateReq, db: Session = Depends(get_db)):
    return auth.create_user(user, db)


@router.post("/signin", response_model=UserLoginRes)
def login_user(user: UserLoginReq, db: Session = Depends(get_db)):
    return auth.login_user(user, db)
