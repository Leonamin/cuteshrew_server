from tokenize import group
from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

from .. import models, schemas
import time


def get_page(post_id: int, page_num: int, count_per_page: int, db: Session):
    posting = db.query(models.Posting).filter(models.Posting.id == post_id)

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting with the id {post_id} not found")
    comments = db.query(models.Comment)\
        .filter(models.Comment.post_id == post_id)\
        .order_by(models.Comment.group_id)\
        .offset((page_num - 1) * count_per_page)\
        .limit(count_per_page)\
        .all()

    return comments


def create_comment(post_id: int, request: schemas.CommentCreate, db: Session, request_user: schemas.User):
    user = db.query(models.User).filter(
        models.User.email == request_user.email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User name: {request_user.nickname}, email: {request_user.email} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.id == post_id
    )

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting number: {post_id} not found")

    new_comment = models.Comment(
        user_id=user.first().id,
        comment=request.comment,
        created_at=int(time.time()),
        post_id=post_id,
        comment_class=0,
        order=0,
        group_id=0
    )
    db.add(new_comment)
    # print(f"add 후 {new_comment.id}")

    db.commit()
    # print(f"commit 후 {new_comment.id}") 여기서 부터 생기네

    db.refresh(new_comment)
    # print(f"refresh 후 {new_comment.id}")

    comment = db.query(models.Comment).filter(
        models.Comment.id == new_comment.id)
    comment.update({'group_id': new_comment.id})
    db.commit()
    return 'created'


def create_reply(post_id: int, group_id: int, request: schemas.CommentCreate, db: Session, request_user: schemas.User):
    user = db.query(models.User).filter(
        models.User.email == request_user.email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User name: {request_user.nickname}, email: {request_user.email} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.id == post_id
    )

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posting number: {post_id} not found")

    order_num = db.query(models.Comment)\
        .filter(models.Comment.post_id == post_id,
                models.Comment.group_id == group_id)\
        .order_by(models.Comment.order.desc()).first().order

    print(f"order num= {order_num}")

    new_comment = models.Comment(
        user_id=user.first().id,
        comment=request.comment,
        created_at=int(time.time()),
        post_id=post_id,
        comment_class=1,
        order=order_num+1,
        group_id=group_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return 'created'
