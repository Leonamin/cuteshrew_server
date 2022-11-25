from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

from app.dependency import Authority
from .. import models, schemas
import time


def get_all(community_count: int, db: Session):
    if (community_count > 0) :
        communities_db = db.query(models.Community).limit(community_count).all()
    else :
        communities_db = db.query(models.Community).all()
        
    communities = []    
    
    for community in communities_db:
        community.postings = db.query(models.Posting).filter(
            models.Posting.community_id == community.id).order_by(models.Posting.id.desc()).limit(5).all()
        postings = []
        for posting in community.postings:
            comment_count = db.query(models.Comment)\
                .filter(models.Comment.post_id == posting.id).count()
            posting_preview = schemas.PostingPreview(\
                id=posting.id,\
                title=posting.title,\
                is_locked=posting.is_locked,\
                comment_count=comment_count)
            postings.append(posting_preview)
        show_community = schemas.ShowCommunity(\
            id=community.id,\
            name=community.name,\
            showname=community.showname,\
            authority=community.authority,\
            created_at=community.created_at,\
            published_at=community.published_at,\
            postings=postings,\
            postings_count=len(postings))
        communities.append(show_community)
        
    return communities


def get_page(name: str, page_num: int, count_per_page: int, db: Session):

    community = db.query(models.Community).filter(
        models.Community.name == name).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'detail': f"Community with the name {name} is not available"})

    community.postings = db.query(models.Posting).filter(
        models.Posting.community_id == community.id)\
        .order_by(models.Posting.id.desc())\
        .offset((page_num - 1) * count_per_page)\
        .limit(count_per_page)\
        .all()
    postings = []
    for posting in community.postings:
        comment_count = db.query(models.Comment)\
            .filter(models.Comment.post_id == posting.id).count()
        posting_preview = schemas.PostingPreview(\
            id=posting.id,\
            title=posting.title,\
            is_locked=posting.is_locked,\
            comment_count=comment_count)
        postings.append(posting_preview)
    show_community = schemas.ShowCommunity(\
            id=community.id,\
            name=community.name,\
            showname=community.showname,\
            authority=community.authority,\
            created_at=community.created_at,\
            published_at=community.published_at,\
            postings=postings,\
            postings_count=len(postings))

    return show_community


def create(request: schemas.CommunityBase, db: Session, request_user: schemas.User):
    # 유저 검사
    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not (user.first().authority.value >= Authority.SUB_ADMIN.value):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User has low authority {user.first().authority}")

    new_community = models.Community(name=request.name,
                                     showname=request.showname,
                                     authority=request.authority,
                                     created_at=int(time.time()),
                                     published_at=int(time.time()))
    db.add(new_community)
    db.commit()
    db.refresh(new_community)
    return new_community


def destroy(id: int, db: Session, request_user: schemas.User):
    user = db.query(models.User).filter(
        models.User.email == request_user.email)

    if not (user.first().authority.value >= Authority.SUB_ADMIN.value):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User has low authoriy {user.first().authority}")

    community = db.query(models.Community).filter(models.Community.id == id)

    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the id {id} not found")

    community.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def show(name: str, db: Session):

    community = db.query(models.Community).filter(
        models.Community.name == name).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'detail': f"Community with the name {name} is not available"})

    community.postings = db.query(models.Posting).filter(
        models.Posting.community_id == community.id).order_by(models.Posting.id.desc()).limit(5).all()

    return community
