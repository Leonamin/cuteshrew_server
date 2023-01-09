from typing import Optional
from sqlalchemy.orm import Session, exc
from fastapi import HTTPException

from app import database
from app.exceptions import DatabaseError, UnknownError
from app.models.models import Posting, Comment

async def get_postings_by_user_id(
    user_id: int, load_count: int, skip_until_id: Optional[int] = None):
    try:
        db: Session = next(database.get_db())
        if skip_until_id != None:
            postings: Posting = db.query(Posting)\
                .filter(Posting.user_id == user_id)\
                .order_by(Posting.id.desc())\
                .where(Posting.id < skip_until_id)\
                .limit(load_count)\
                .all()
        else:
            postings: Posting = db.query(Posting)\
                .filter(Posting.user_id == user_id)\
                .order_by(Posting.id.desc())\
                .limit(load_count)\
                .all()
        return postings
    # TODO Exception 순서 확인 캐치되는 종류를 알아봐야 겠다.
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)


async def get_comments_by_user_id(
    user_id: int, load_count: int, skip_until_id: Optional[int] = None):
    try:
        db: Session = next(database.get_db())
        if skip_until_id != None:
            comments: Comment = db.query(Comment)\
                .filter(Comment.user_id == user_id)\
                .order_by(Comment.id.desc())\
                .where(Comment.id < skip_until_id)\
                .limit(load_count)\
                .all()
        else:
            comments: Comment = db.query(Comment)\
                .filter(Comment.user_id == user_id)\
                .order_by(Comment.id.desc())\
                .limit(load_count)\
                .all()
        return comments
    # TODO Exception 순서 확인 캐치되는 종류를 알아봐야 겠다.
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)