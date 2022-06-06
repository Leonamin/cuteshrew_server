from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
from .. import models, schemas

def get_all(db: Session):
    communities = db.query(models.Community).all()
    return communities

def create(request: schemas.CommunityBase, db: Session):
    new_community = models.Community(name=request.name, type=request.type)
    db.add(new_community)
    db.commit()
    db.refresh(new_community)
    return new_community