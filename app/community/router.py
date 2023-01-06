from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/community",
    tags=['community']
)
default_community_count = 5
default_count_per_page = 15

# 커뮤니티
# 일반적으로 메인 페이지에 쓰이고 0개면 모든 커뮤니티를 불러온다

@router.get('', response_model_exclude_none=True)
def all(community_count: Optional[int] = 0):
    pass
# TODO 어드민만 생성 가능하게 변경


@router.post('', status_code=status.HTTP_201_CREATED)
def create():
    pass
# 204 에러는 Content-Length를 가질 수 없다


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int):
    pass

# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{name}/page/{page_num}', response_model_exclude_none=True)
def get_page(name: str, page_num: int, count_per_page: Optional[int] = default_count_per_page):
    pass