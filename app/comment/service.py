import time
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query, exc

from app import database
from app.exceptions import DatabaseError, UnknownError
from app.models.models import Comment
from app.comment.exceptions import CommentNotFound

async def get_comment_by_comment_id(comment_id: int):
    try:
        db: Session = next(database.get_db())
        comment: Comment = db.query(Comment)\
            .filter(Comment.id == comment_id).first()
        if not comment:
            raise CommentNotFound()
        return comment
    # TODO Exception 순서 확인 캐치되는 종류를 알아봐야 겠다.
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)


async def get_comments_by_posting_id(
    posting_id: int, load_count: int, skip_offset: Optional[int] = None
):
    try:
        db: Session = next(database.get_db())
        comment: Comment = db.query(Comment)\
            .filter(Comment.post_id == posting_id)\
            .order_by(Comment.created_at.desc())\
            .offset(skip_offset)\
            .limit(load_count)\
            .all()
        if not len(comment):
            raise CommentNotFound()
        return comment
    # TODO Exception 순서 확인 캐치되는 종류를 알아봐야 겠다.
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)
    
async def create_comment(
    posting_id: int,
    user_id: int,
    comment: str,
):
    try:
        db: Session = next(database.get_db())
        new_comment = Comment(
        user_id=user_id,
        comment=comment,
        created_at=int(time.time()),
        post_id=posting_id,
        comment_class=0,
        order=0,
        group_id=0
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        comment = db.query(Comment).filter(
            Comment.id == new_comment.id)
        # 한 댓글 그룹의 대표니까 group_id는 댓글의 id로 설정
        comment.update({'group_id': new_comment.id})
        db.commit()
        return new_comment
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)


async def create_reply(
    posting_id: int,
    user_id: int,
    group_id: int,
    comment_class: int,
    comment: str,
):
    try:
        db: Session = next(database.get_db())
        
        # 같은 그룹 같은 계층에서 가장 마지막 댓글의 순서를 가져온다.
        last_comment_order = db.query(Comment)\
        .filter(Comment.group_id == group_id,
                Comment.comment_class == comment_class)\
        .order_by(Comment.order.desc()).first().order
        
        new_reply = Comment(
        user_id=user_id,
        comment=comment,
        created_at=int(time.time()),
        post_id=posting_id,
        comment_class=comment_class,
        order=last_comment_order,
        group_id=group_id
        )
        db.add(new_reply)
        db.commit()
        db.refresh(new_reply)
        return new_reply
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)


async def update_comment_by_id(
    comment_id: int,
    comment: str
):
    try:
        db: Session = next(database.get_db())
        
        comment: Query = db.query(Comment).filter(Comment.id == comment_id)
        if not comment:
            raise CommentNotFound()
        comment.update({'comment':comment})
        db.commit()
        return comment.first()
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)


async def delete_comment_by_id(
    comment_id: int
):
    try:
        db: Session = next(database.get_db())
        
        comment = db.query(Comment).filter(Comment.id == comment_id)
        if not comment:
            raise CommentNotFound()
        comment.delete(synchronize_session=False)
        db.commit()
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)