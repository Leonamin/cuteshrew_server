from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
from app.dependency import Authority
from app.hashing import Hash

from app.oauth2 import get_current_user
from .. import models, schemas
import time

# 속한 커뮤니티의 게시글 로딩
# /community/general/12313


def get_all(name: str, db: Session):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    postings = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id).all()

    return postings


def get_post(name: str, post_id: int, password: str, db: Session):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id, models.Posting.id == post_id).first()

    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting with the id {post_id} not found on {name} Community")
    # https://auth0.com/blog/forbidden-unauthorized-http-status-codes/
    if posting.is_locked:
        if password == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"need password")
        if not Hash.verify(posting.password, password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Invalid password")
    return posting

# FIXME password가 공백이여도 암호가 생성된다 nullable로 만들어야해!


def create_post(name: str, reqeust: schemas.PostingCreate, db: Session, request_user: schemas.User):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    # TODO 게시판 허용 권한 검사
    if not (user.first().authority.value >= community.first().authority.value):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User has low authoriy {user.first().authority}")

    new_post = models.Posting(
        title=reqeust.title,
        body=reqeust.body,
        published_at=int(time.time()),
        updated_at=int(time.time()),
        is_locked=reqeust.is_locked,
        password=Hash.bcrypt(reqeust.password),
        community_id=community.first().id,
        user_id=user.first().id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return "Post is created!"


def update_post(name: str, post_id: int, reqeust: schemas.PostingCreate, db: Session, request_user: schemas.User):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id, models.Posting.id == post_id)

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting with the id {post_id} not found on {name} Community")

    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not user.first().id == posting.first().user_id:
        if not user.first().authority.value >= Authority.SUB_ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User has low authoriy {user.first().authority}")

    posting.update(reqeust.dict())
    posting.update({'password': Hash.bcrypt(reqeust.password)})
    posting.update({'updated_at': int(time.time())})
    db.commit()
    return 'updated'


def delete_post(name: str, post_id: int, db: Session, request_user: schemas.User):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id, models.Posting.id == post_id)

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting with the id {post_id} not found on {name} Community")

    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not user.first().id == posting.first().user_id:
        if not user.first().authority.value >= Authority.SUB_ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User has low authoriy {user.first().authority}")

    posting.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
