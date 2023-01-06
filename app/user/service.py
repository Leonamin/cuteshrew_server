from fastapi import Depends
from sqlalchemy.orm import Session
from app import database
from app.user.exceptions import UserNotFoundException

# FIXME User 옮겨야함
from app.models.models import User

# Depends는 FastAPI의 엔드포인트에서만 사용할 수 있다
# Depends와 연결되서 파라미터 단위에서 계속 Depends될 경우 상관 없으나 
# 얘처럼 따로 일반 함수로써 사용되는 경우는 Depends가 동작이 안된다.
# 그래서 의존성 주입을 어떻게 할까 찾아보다가 next()를 붙이는 방법을 찾았다
# https://stackoverflow.com/questions/65982681/how-to-access-the-database-from-unit-test-in-fast-api
# 근데 이것을 했을 때 문제점이 뭐가 있을지 모르겠다.
async def get_user_by_user_name(
    user_name: str,
):
    db: Session = next(database.get_db())
    user = db.query(User).filter(User.nickname == user_name).first()
    return user


async def get_user_by_user_email(
    user_email: str,
):
    db: Session = next(database.get_db())
    user = db.query(User).filter(User.email == user_email).first()
    return user
