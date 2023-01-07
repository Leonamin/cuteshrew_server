import time
from sqlalchemy.orm import Session
from app import database
from app.dependency import Authority


# FIXME Community 옮겨야함
from app.models.models import Community

async def get_community_by_name(
    community_name: str,
):
    db: Session = next(database.get_db())
    community = db.query(Community).filter(Community.name == community_name).first()
    return community

async def create_community(
    community_name: str,
    community_showname: str,
    authority: Authority,
):
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
    
    return new_community

async def delete_community(
    community_name: str
):
    db: Session = next(database.get_db())
    community = db.query(Community).filter(Community.name == community_name)
    db: Session = next(database.get_db())
    community.delete(synchronize_session=False)
    db.commit()