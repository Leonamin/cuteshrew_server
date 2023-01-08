import time
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query, exc

from app import database
from app.exceptions import DatabaseError, HashTypeError, HashValueError, UnknownError
from app.auth.utils import Hash
from app.models.models import Community, Posting
from app.posting.exceptions import PostingNotFound, InvalidPasswordException, NeedPasswordException

# 서비스의 역할
# 데이터 검증은 하지 않는다.
# 데이터 읽기/쓰기에 필요한 동작만 한다. (예 - 검색, 읽기 쓰기 시 DB에 맞는 데이터 변환)
# 서비스 계층 <-> 데이터베이스 계층 이므로
# 서비스 계층으로 들어온 데이터를 데이터베이스에 맞게 입출력하는 절차만 한다.
# 나중에 서버가 대형화 되면 그 때 또 도메인 계층을 제대로 만들겠지

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
    
# 검사 로직 없이 데이터 반환
async def get_postings_by_community_id(community_id: int, load_count: int, skip_offset: Optional[int] = None):
    try:
        db: Session = next(database.get_db())
        postings: Posting = db.query(Posting)\
            .filter(Posting.community_id == community_id)\
            .order_by(Posting.published_at.desc())\
            .offset(skip_offset)\
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

async def get_posting_count_by_community_id(
    community_id: int
):
    db: Session = next(database.get_db())
    return db.query(Posting).filter(Posting.community_id == community_id).count()

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
    
# 검사 로직 없이 데이터 반환
async def delete_posting_by_id(posting_id: int):
    try:
        db: Session = next(database.get_db())
        posting = db.query(Posting).filter(
            Posting.id == posting_id,
        )
        if not posting.first():
            raise PostingNotFound()
        posting.delete(synchronize_session=False)
        db.commit()
    except HTTPException as e:
        raise e
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)
    
async def update_posting(
    posting_id: int,
    community_id: int,
    title: str,
    body: str,
    is_locked: bool,
    password: Optional[str] = None,
):  
    try:
        db: Session = next(database.get_db())

        posting: Query = db.query(Posting).filter(Posting.id == posting_id)
        if not posting.first():
            raise PostingNotFound()
        if (is_locked):
                password = Hash.bcrypt(password)
        # 이게 posting 쿼리로 잡힌 모든 테이블을 업데이트 하는건데
        # id가 중복될리는 없으니까 상관 없겠지?
        posting.update({
            'community_id' : community_id,
            'title' : title,
            'body' : body,
            'is_locked' : is_locked,
            'password' : password,
            'updated_at' : int(time.time())
        })
        db.commit()
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
    return 'updated'