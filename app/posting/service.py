import time
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query, exc

from app import database
from app.exceptions import DatabaseError, HashTypeError, HashValueError, UnknownError
from app.auth.utils import Hash
from app.models.models import Community, Posting
from app.posting.exceptions import PostingNotFound, InvalidPasswordException, NeedPasswordException
    
# 검사 로직 없이 데이터 반환
async def get_posting_by_id(posting_id: int):
    try:
        db: Session = next(database.get_db())
        posting: Posting = db.query(Posting)\
            .filter(Posting.id == posting_id).first()
        if not posting:
            raise PostingNotFound()
        return posting
    # TODO Exception 순서 확인 캐치되는 종류를 알아봐야 겠다.
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)

# 무적권 is_locked가 true일 때만 password가 None다
async def create_posting(
    community_id: int,
    user_id: int,
    title: str,
    body: str,
    is_locked: bool,
    password: Optional[str] = None,
):
    try:
        # 이렇게하면 None일 때 bcryt를 안할거다.
        # 그런데 이미 검증 후 들어오는 것으로 동작해야하는데
        # 여기서 추가 검증을 넣으면 비효율적인가?
        if (is_locked):
            password = Hash.bcrypt(password)
            
        new_posting = Posting(
            title=title,
            body=body,
            published_at=int(time.time()),
            updated_at=int(time.time()),
            is_locked=is_locked,
            password=password,
            community_id=community_id,
            user_id=user_id,
        )
        db: Session = next(database.get_db())
        db.add(new_posting)
        db.commit()
        db.refresh(new_posting)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HashValueError()
    except TypeError as e:
        raise HashTypeError()
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)