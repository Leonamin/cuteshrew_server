from typing import Mapping, Optional
from fastapi import APIRouter, Depends, status

from app.community import dependency as community_dependency
from app.posting.dependency import valid_posting_id, verify_posting, can_user_write_posting
from app.posting.schemas import ResponsePostingDetail, RequestPostingCreate
from app.posting import service
from app.posting.exceptions import UnauthorizedException
from app.community import dependency as community_dependency
from app.user import dependency as user_dependency

router = APIRouter(
    prefix="/community/{community_name}",
    tags=['posting']
)


@router.get("/{id}", response_model=ResponsePostingDetail)
async def get_post(
    community: Mapping = Depends(community_dependency.valid_community_name),
    posting: Mapping = Depends(verify_posting)
):
    return posting


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(
    new_posting: RequestPostingCreate,
    community: Mapping = Depends(
        community_dependency.valid_community_name),
    user: Mapping = Depends(user_dependency.get_current_user_info)
):
    if can_user_write_posting(community, user):
        print(new_posting.password)
        await service.create_posting(
            community.id,
            user.id,
            new_posting.title,
            new_posting.body,
            new_posting.is_locked,
            new_posting.password
        )
    else:
        raise UnauthorizedException()
