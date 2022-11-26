from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

from app.dependency import Authority
from .. import models, new_schemas
import time

# 일반적으로 메인 페이지에 쓰이고 0개면 모든 커뮤니티를 불러온다


def get_all(community_count: int, db: Session):
    if (community_count > 0):
        communities_db = db.query(
            models.Community).limit(community_count).all()
    else:
        communities_db = db.query(models.Community).all()

    communities = []

    # 커뮤니티 게시글 최신순으로 개수 한정해서 넣어주기
    for community in communities_db:
        community.postings = db.query(models.Posting).filter(
            models.Posting.community_id == community.id).order_by(models.Posting.id.desc()).limit(5).all()
        postings = []
        # 게시글 응답 스키마 생성 후 리스트에 추가
        for posting in community.postings:
            comment_count = db.query(models.Comment)\
                .filter(models.Comment.post_id == posting.id).count()
            posting_preview = new_schemas.PostingPreview.from_orm(posting)
            posting_preview.comment_count = comment_count
            postings.append(posting_preview)
        show_community = new_schemas.ResponseShowCommunity.from_orm(community)
        show_community.postings = postings
        show_community.posting_count = len(postings)
        communities.append(show_community)

    return communities

# 개별 커뮤니티 화면에서 요청하게 될 함수


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
        posting_preview = new_schemas.PostingPreview.from_orm(posting)
        posting_preview.comment_count = comment_count
        postings.append(posting_preview)
    show_community = new_schemas.ResponseShowCommunity.from_orm(community)
    show_community.postings = postings
    show_community.posting_count = len(postings)

    return show_community


def create(request: new_schemas.CommunityCreate, db: Session, request_user: new_schemas.UserBase):
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


def destroy(id: int, db: Session, request_user: new_schemas.UserBase):
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
