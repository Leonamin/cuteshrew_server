import time
from sqlalchemy.orm import Session, Query
from app.db import database
from app.dependency import Authority
from sqlalchemy import exc

# FIXME Community 옮겨야함
from app.models.models import Community

from app.exceptions import DatabaseError
from app.community.exceptions import CommunityNotFound

async def get_communities(load_count: int):
    try:
        db: Session = next(database.get_db())
        communities = db.query(Community)\
            .limit(load_count).all()
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    return communities
        

async def get_community_by_name(
    community_name: str,
):
    try:
        db: Session = next(database.get_db())
        community = db.query(Community).filter(Community.name == community_name).first()
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error') 
    return community

async def create_community(
    community_name: str,
    community_showname: str,
    authority: Authority,
):
    try:
        db: Session = next(database.get_db())
        new_community = Community(
            name=community_name,
            showname=community_showname,
            authority=authority,
            created_at=int(time.time()),
            published_at=int(time.time()),
        )

        db.add(new_community)
        db.commit()
        db.refresh(new_community)
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error')
    
    return new_community

# dir(exc) 하면 SQLAlchemy 에러 전체 확인 가능
async def delete_community(
    community_id: int
):
    try:
        db: Session = next(database.get_db())
        community: Query = db.query(Community).filter(Community.id == community_id)
        community.delete(synchronize_session=False)
        db.commit()
    except exc.SQLAlchemyError as e:
        raise DatabaseError(detail='sqlalchemy error') 