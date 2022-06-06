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

def destroy(id: int, db: Session):
    community = db.query(models.Community).filter(models.Community.id == id)

    if not community.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Community with the id {id} not found")

    community.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)