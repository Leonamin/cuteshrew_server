from typing import Mapping
from fastapi import APIRouter, Depends, status

from app.community import dependency as community_dependency
from app.posting.dependency import valid_posting_id
from app.posting.schemas import ResponsePostingDetail

router = APIRouter(
    prefix="/community/{community_name}",
    tags=['posting']
)


@router.get("/{id}", response_model=ResponsePostingDetail)
async def get_post(
        posting: Mapping = Depends(valid_posting_id)
):
    return posting


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post():
    pass


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post():
    pass


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post():
    pass
