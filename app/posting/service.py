from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query, exc

from app import database
from app.exceptions import DatabaseError, HashTypeError, HashValueError, UnknownError
from app.auth.utils import Hash
from app.models.models import Community, Posting
from app.posting.exceptions import PostingNotFound, InvalidPasswordException, NeedPasswordException


async def get_posting(
        community_id: int,
        posting_id: int,
        password: Optional[str]):
    try:
        db: Session = next(database.get_db())
        posting: Posting = db.query(Posting)\
            .filter(
                Posting.community_id == community_id,
                Posting.id == posting_id).first()
        if not posting:
            raise PostingNotFound()
        if posting.is_locked:
            if password == None:
                raise NeedPasswordException()
            if not Hash.verify(posting.password, password):
                raise InvalidPasswordException()
        return posting
    # TODO Exception 순서 확인 캐치되는 종류를 알아봐야 겠다.
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HashValueError()
    except TypeError as e:
        print(e)
        raise HashTypeError()
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e)
