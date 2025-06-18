from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import AuthSignInReq, AuthSignInRes, AuthSignUpReq, AuthSignUpRes
from app.services import auth


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup", response_model=AuthSignUpRes)
def create_user(user: AuthSignUpReq, db: Session = Depends(get_db)):
    return auth.create_user(user, db)


@router.post("/signin", response_model=AuthSignInRes)
async def login_user(
    request: Request,
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db)
) -> AuthSignInRes:
    # 1. 폼 데이터로 들어온 경우 (Swagger UI)
    if password is not None:
        return auth.login_user(AuthSignInReq(user_id=username, password=password), db)
    # 2. JSON 바디로 들어온 경우 (실제 서비스/테스트)
    else:
        data = await request.json()
        loginReq = AuthSignInReq(**data)
        return auth.login_user(loginReq, db)
