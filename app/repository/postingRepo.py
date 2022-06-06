from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
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


def get_post(name: str, post_id: int, db: Session):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id, models.Posting.id == post_id)

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Positing with the id {post_id} not found on {name} Community")

    return posting


def create_post(name: str, reqeust: schemas.PostingBase, db: Session):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    new_post = models.Posting(
        title=reqeust.title,
        body=reqeust.body,
        published_at=time.time(),
        updated_at=time.time(),
        community_id=community.first().id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post(name: str, post_id: int, reqeust: schemas.PostingBase, db: Session):
    community = db.query(models.Community).filter(
        models.Community.name == name)
    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the name {name} not found")

    posting = db.query(models.Posting).filter(
        models.Posting.community_id == community.first().id, models.Posting.id == post_id)

    if not posting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Positing with the id {post_id} not found on {name} Community")

    posting.update(reqeust.dict())
    posting.update({'updated_at': time.time()})
    db.commit()
    return 'updated'
