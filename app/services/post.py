from sqlalchemy.orm import Session

from app.core.exceptions import UserNotFoundException
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostDraftRes


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
