from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserReadRes

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserReadRes)
def read_me(current_user: User = Depends(get_current_user)):
    return UserReadRes(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        thumbnail_url=getattr(current_user, "thumbnail_url", None)
    )
