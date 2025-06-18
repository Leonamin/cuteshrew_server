from passlib.context import CryptContext

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailException
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user import UserCreateReq, UserCreateRes
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utils


def get_secret_key() -> str:
    return settings.SECRET_KEY


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

# Service


def create_user(user: UserCreateReq, db: Session) -> UserCreateRes:
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

        return UserCreateRes(id=new_user.id)
    except Exception as e:
        db.rollback()
        raise e
