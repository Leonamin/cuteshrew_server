from uuid import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import (
    PostNotAuthorizedException,
    PostNotFoundException,
    UserNotFoundException,
)
from app.models.post import Post
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.post import PostDetailRes, PostDraftRes, PostUpdateReq, PostUpdateRes


def create_draft(
    db: Session,
    user_id: int,
) -> PostDraftRes:
    is_user_exists = db.query(User).filter(User.id == user_id).first()
    if not is_user_exists:
        raise UserNotFoundException()
    new_draft = Post(
        user_id=user_id,
        title="",
        content="",
        is_draft=True,
    )
    db.add(new_draft)
    db.commit()
    db.refresh(new_draft)
    return PostDraftRes(id=str(new_draft.id))


def update_post(
    db: Session,
    post_id: str,
    post: PostUpdateReq,
    user_id: int,
) -> PostUpdateRes:
    is_user_exists = db.query(User).filter(User.id == user_id).first()
    if not is_user_exists:
        raise UserNotFoundException()
    db_post = db.query(Post).filter(Post.id == UUID(post_id)).first()
    if not db_post:
        raise PostNotFoundException()
    if db_post.user_id != user_id:
        raise PostNotAuthorizedException()
    
    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content
    if post.thumbnail_url:
        db_post.thumbnail_url = post.thumbnail_url
    if post.publish:
        db_post.publish = post.publish
    db.commit()
    db.refresh(db_post)
    return PostUpdateRes(id=str(db_post.id))

def get_post_detail(
    db: Session,
    post_id: str,
) -> PostDetailRes:
    db_post = db.query(Post).filter(Post.id == UUID(post_id)).first()
    if not db_post:
        raise PostNotFoundException()
    
    if db_post.is_draft:
        raise PostNotFoundException()

    db_user = db.query(User).filter(User.id == db_post.user_id).first()
    db_user_profile = db.query(UserProfile).filter(UserProfile.user_id == db_post.user_id).first()
    user_name = ''
    user_thumbnail_url = ''

    if db_user:
        user_name = db_user.name
    if db_user_profile:
        user_thumbnail_url = db_user_profile.thumbnail_url

    return PostDetailRes(
        id=str(db_post.id),
        title=db_post.title,
        content=db_post.content,
        thumbnail_url=db_post.thumbnail_url,
        created_at=db_post.created_at,
        view_count=0,
        like_count=0,
        comment_count=0,
        writer_id=db_post.user_id,
        writer_name=user_name,
        writer_thumbnail_url=user_thumbnail_url,
    )