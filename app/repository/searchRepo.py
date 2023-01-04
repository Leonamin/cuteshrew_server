from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import models


from ..schemas import new_schemas

# FIXME 생각해보니 Response 모델 하나로 돌려쓰는건 바보같은 짓이고 세부적으로 나눠야할 필요가 있다.
# user_id와 user_name 둘중 하나는 있어야함
# start_post_id는 원래 해당 포스팅 부터 시작하게하려고 했으나 기술적인 이유로 포기 그냥 필터링 된 개수에서 n번부터 시작함
# 2022-11-17 해결 방법은 매우 간단하게도 .where(조건)을 사용하면 조건을 만족하는 것 이후부터 찾을 수 있다!
# load_page_num은 load_page_num
# 포스팅은 일단 user가 있어야 반환
# user는 user id, nickname으로 검색해서 찾는다

def search_posts_by_user(user_id: int, user_name: str, start_id: int, load_page_num: int, db: Session):
    if (user_id == None and user_name == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found this user")

    if (user_id != None):
        user = db.query(models.User)\
            .filter(models.User.id == user_id)\
            .first()
        if not user:
            if (user_name == None):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Not found this user")

    if (user_name != None):
        user = db.query(models.User)\
            .filter(models.User.nickname == user_name)\
            .first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Not found this user")
        user_id = user.id

    if (start_id != None):
        postings_db = db.query(models.Posting)\
            .filter(
            models.Posting.user_id == user_id)\
            .order_by(models.Posting.id.desc())\
            .where(models.Posting.id < start_id)\
            .limit(load_page_num)\
            .all()
    else:
        postings_db = db.query(models.Posting)\
            .filter(
            models.Posting.user_id == user_id)\
            .order_by(models.Posting.id.desc())\
            .limit(load_page_num)\
            .all()
    # 게시글 개수 구하기
    posting_counts = db.query(models.Posting)\
        .filter(
        models.Posting.user_id == user_id).count()

    # 댓글 개수 구해서 PostingPreviewResponse에 추가
    postings = []
    for posting in postings_db:
        comment_count = db.query(models.Comment)\
            .filter(models.Comment.post_id == posting.id).count()
        posting_response = new_schemas.ResponsePostingPreview.from_orm(posting)
        posting_response.comment_count = comment_count
        posting_response.user_id = None
        
        if (posting_response.posting.own_community is not None):
                posting_response.own_community.authority = None
                posting_response.own_community.created_at = None
                posting_response.own_community.published_at = None
        posting_response.own_community.authority = None
        posting_response.own_community.created_at = None
        posting_response.own_community.published_at = None
        postings.append(posting_response)

    return new_schemas.ResponsePostingList(posting_count=posting_counts, postings=postings)
    # return postings

# user_id와 user_name 둘중 하나는 있어야함
# start_comment_id는 원래 해당 포스팅 부터 시작하게하려고 했으나 기술적인 이유로 포기 그냥 필터링 된 개수에서 n번부터 시작함
# 2022-11-17 해결 방법은 매우 간단하게도 .where(조건)을 사용하면 조건을 만족하는 것 이후부터 찾을 수 있다!
# load_page_num은 load_page_num
# 포스팅은 일단 user가 있어야 반환
# user는 user id, nickname으로 검색해서 찾는다


def search_comments_by_user(user_id: int, user_name: str, start_id: int, load_page_num: int, db: Session):
    if (user_id == None and user_name == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found this user")

    if (user_id != None):
        user = db.query(models.User)\
            .filter(models.User.id == user_id)\
            .first()
        if not user:
            if (user_name == None):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Not found this user")

    if (user_name != None):
        user = db.query(models.User)\
            .filter(models.User.nickname == user_name)\
            .first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Not found this user")
        user_id = user.id

    if (start_id != None):
        comments_db = db.query(models.Comment)\
            .filter(
            models.Comment.user_id == user_id)\
            .order_by(models.Comment.id.desc())\
            .where(models.Comment.id < start_id)\
            .limit(load_page_num)\
            .all()
    else:
        comments_db = db.query(models.Comment)\
            .filter(
            models.Comment.user_id == user_id)\
            .order_by(models.Comment.id.desc())\
            .limit(load_page_num)\
            .all()
    comment_counts = db.query(models.Comment)\
        .filter(
        models.Comment.user_id == user_id).count()
        
    comments = []
    
    for comment in comments_db:
        comment_response = new_schemas.ResponseComment.from_orm(comment)
        # 삭제 되었을 경우 posting이 None이기 때문에 하위 필드 접근이 안된다.
        if (comment_response.posting is not None):
            if (comment_response.posting.own_community is not None):
                comment_response.posting.own_community.authority = None
                comment_response.posting.own_community.created_at = None
                comment_response.posting.own_community.published_at = None
            comment_response.posting.user_id = None
        comments.append(comment_response)

    return new_schemas.ResponseCommentList(comment_count=comment_counts, comments=comments)
