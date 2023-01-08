
from typing import Mapping, Optional
from fastapi import Depends, HTTPException
from pydantic import SecretStr

from app.dependency import Authority
from app.exceptions import HashTypeError, HashValueError, UnknownError
from app.posting import service
from app.posting.constants import MAX_POSTING_LOAD_COUNT
from app.posting.schemas import RequestPostingCreate
from app.posting.exceptions import InvalidLoadCountException, PostingNotFound, NeedPasswordException, InvalidPasswordException, UnauthorizedException
from app.community import dependency as community_dependency
from app.user import dependency as user_dependency

from app.auth.utils import Hash


# id를 통해 포스팅이 존재하는지 확인
async def valid_posting_id(
    id: int,
) -> Mapping:
    posting = await service.get_posting_by_id(id)

    if not posting:
        raise PostingNotFound()
    return posting

# 가져온 포스팅의 비밀번호가 올바른지 확인
async def verify_posting(
    password: Optional[SecretStr] = None,
    posting: Mapping = Depends(valid_posting_id)
) -> Mapping:
    if not posting.is_locked:
        return posting
    try:
        if not password:
            raise NeedPasswordException()
        if not Hash.verify(posting.password, password.get_secret_value()):
            raise InvalidPasswordException()
        return posting
        
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HashValueError()
    except TypeError as e:
        raise HashTypeError()
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)

def can_user_write_posting(
    community: Mapping,
    user: Mapping
) -> Mapping:
    if (community.authority.value > user.authority.value):
        raise UnauthorizedException()
    return community

async def can_user_delete_posting(
    community: Mapping = Depends(community_dependency.valid_community_name),
    posting: Mapping = Depends(valid_posting_id),
    user: Mapping = Depends(user_dependency.get_current_user_info),
) -> Mapping:
    # 유저 본인이 아니거나
    # 관리자가 강제 삭제 권한이 커뮤니티 보다 낮으면 접근 불가
    if not user.id == posting.user_id:
        # 관리자가 아니거나 관리자여도 접근 금지 커뮤니티면 불가
        # TODO 관리자 권한 체크하는 의존성 만들어야함
        if (user.authority.value < Authority.SUB_ADMIN.value) or \
        (user.authority.value < community.authority.value):
            raise UnauthorizedException()
    return posting

# 오직 게시글 작성자만 수정할 수 있음
# 게시글 작성자는 업데이트 하려는 커뮤니티 기존이든 신규든 권한이 있어야 수정이 가능함
def can_user_modify_posting(
    community: Mapping,
    user: Mapping,
    posting: Mapping
) -> Mapping:
    if (community.authority.value > user.authority.value) or (posting.user_id != user.id):
        raise UnauthorizedException()
    return community

# 최대 개수 제한
def valid_load_cound(load_count: Optional[int] = None) -> int:
    if load_count == None:
        load_count = MAX_POSTING_LOAD_COUNT
    if (load_count > MAX_POSTING_LOAD_COUNT or load_count <= 0):
        raise InvalidLoadCountException()
    return load_count