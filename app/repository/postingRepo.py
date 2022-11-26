from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
from app.dependency import Authority
from app.hashing import Hash

from .. import models, new_schemas
import time


def get_post(name: str, post_id: int, password: str, db: Session):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    posting_db = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id, models.Posting.id == post_id).first()

    if not posting_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting with the id {post_id} not found on {name} Community")
    # https://auth0.com/blog/forbidden-unauthorized-http-status-codes/
    if posting_db.is_locked:
        if password == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"need password")
        if not Hash.verify(posting_db.password, password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Invalid password")
    
    posting = new_schemas.ResponsePosting.from_orm(posting_db)
    posting.password = None
    posting.user_id = None
    # posting.own_community.id = None
    posting.own_community.authority = None
    posting.own_community.created_at = None
    posting.own_community.published_at = None
    
    return posting

# FIXME password가 공백이여도 암호가 생성된다 nullable로 만들어야해!


def create_post(name: str, reqeust: new_schemas.PostingCreate, db: Session, request_user: new_schemas.UserBase):
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
    
    # 잠긴 게시물이 아니면 비밀번호 없음
    if (reqeust.is_locked == False) :
        password = None
    else:
        # 잠긴 게시물로 설정해도 비밀번호가 없거나 길이가 0이면 생성금지
        if (reqeust.password is None) or (len(reqeust.password) <= 0):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"password can't be null or empty")
        password = Hash.bcrypt(reqeust.password)

    new_post = models.Posting(
        title=reqeust.title,
        body=reqeust.body,
        published_at=int(time.time()),
        updated_at=int(time.time()),
        is_locked=reqeust.is_locked,
        password=password,
        community_id=community.first().id,
        user_id=user.first().id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return "Post is created!"


def update_post(name: str, post_id: int, reqeust: new_schemas.PostingCreate, db: Session, request_user: new_schemas.UserBase):
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
    # 잠긴 게시물이 아니면 비밀번호 없음
    if (reqeust.is_locked == False) :
        password = None
    else:
        # 잠긴 게시물로 설정해도 비밀번호가 없거나 길이가 0이면 생성금지
        if (reqeust.password is None) or (len(reqeust.password) <= 0):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"password can't be null or empty")
        password = Hash.bcrypt(reqeust.password)
    posting.update({'password': password})
    posting.update({'updated_at': int(time.time())})
    db.commit()
    return 'updated'


def delete_post(name: str, post_id: int, db: Session, request_user: new_schemas.UserBase):
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
