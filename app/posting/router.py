from typing import List, Mapping, Optional
from fastapi import APIRouter, Depends, status

from app.community import dependency as community_dependency
from app.posting.dependency import can_user_modify_posting, valid_posting_id, verify_posting, can_user_write_posting, can_user_delete_posting, valid_load_cound
from app.posting.schemas import ResponsePostingDetail, RequestPostingCreate
from app.posting import service
from app.posting.exceptions import UnauthorizedException
from app.community import dependency as community_dependency
from app.user import dependency as user_dependency

router = APIRouter(
    prefix="/community/{community_name}",
    tags=['posting']
)


@router.get("", response_model=List[ResponsePostingDetail])
async def get_postings(
    community: Mapping = Depends(community_dependency.valid_community_name),
    load_count: int = Depends(valid_load_cound)
):
    postings = await service.get_postings_by_community_id(community.id, load_count)
    return postings


@router.get("/{id}", response_model=ResponsePostingDetail)
async def get_posting(
    community: Mapping = Depends(community_dependency.valid_community_name),
    posting: Mapping = Depends(verify_posting)
):
    return posting


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_posting(
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


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_posting(
    posting: Mapping = Depends(can_user_delete_posting)
):
    await service.delete_posting_by_id(posting.id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_posting(
    new_posting: RequestPostingCreate,
    new_community_name: Optional[str] = None,
    origin_community: Mapping = Depends(
        community_dependency.valid_community_name),
    posting: Mapping = Depends(valid_posting_id),
    user: Mapping = Depends(user_dependency.get_current_user_info)
):
    if new_community_name != None:
        new_community = await community_dependency.valid_community_name(
            new_community_name)
    else:
        new_community = origin_community
    if (can_user_modify_posting(new_community, user, posting)):
        return await service.update_posting(
            posting.id,
            new_community.id,
            new_posting.title,
            new_posting.body,
            new_posting.is_locked,
            new_posting.password
        )
