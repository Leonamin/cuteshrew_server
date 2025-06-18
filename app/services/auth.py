from passlib.context import CryptContext

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailException, InvalidCredentialsException
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.auth import AuthSignInReq, AuthSignInRes, AuthSignUpReq, AuthSignUpRes
from app.config import settings
from app.utils.jwt_utils import create_access_token, create_refresh_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utils


def get_secret_key() -> str:
    return settings.SECRET_KEY


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

# Service


def create_user(user: AuthSignUpReq, db: Session) -> AuthSignUpRes:
    '''유저 생성 `user` 및 `user_profile`에 데이터 생성'''
    # Email 중복 검사
    if db.query(User).filter(User.email == user.email).first():
        raise DuplicateEmailException()
    # 비밀 번호 해싱
    hashed_password = hash_password(user.password)
    try:
        # 1. 유저 생성
        new_user = User(
            email=user.email,
            password=hashed_password,
            name=user.name,
        )
        db.add(new_user)
        db.flush()

        # 2. 유저 프로필 생성
        new_user_profile = UserProfile(
            user_id=new_user.id,
            thumbnail_url=user.thumbnail_url,
            description=user.description,
        )
        db.add(new_user_profile)

        db.commit()
        db.refresh(new_user)
        db.refresh(new_user_profile)

        return AuthSignUpRes(id=new_user.id)
    except Exception as e:
        db.rollback()
        raise e


def login_user(loginReq: AuthSignInReq, db: Session) -> AuthSignInRes:
    '''유저 로그인'''
    # 유저 조회
    db_user = db.query(User).filter(User.email == loginReq.user_id).first()
    if not db_user:
        raise InvalidCredentialsException()

    # 비밀번호 검증
    if not verify_password(loginReq.password, db_user.password):
        raise InvalidCredentialsException()

    # 토큰 생성
    access_token = create_access_token(
        {"user_id": db_user.id, "email": db_user.email, "name": db_user.name})
    refresh_token = create_refresh_token(
        {"user_id": db_user.id, "email": db_user.email, "name": db_user.name})

    return AuthSignInRes(access_token=access_token, refresh_token=refresh_token)
