from typing import Optional, Dict
from pydantic import BaseModel, Field, validator

from app.posting.constants import MAX_POSTING_TITLE_LENGTH
from app.user import schemas as user_schemas
from app.community import schemas as community_schemas

# 맨날 헷갈리는 거지만 아래 처럼 뒤에 ,가 있으면 파싱 에러난다.
# Expecting property name enclosed in double quotes
# {
#     "aaa" : "aaaa",
# }
class RequestPostingCreate(BaseModel):
    title: str = Field(min_length=1, max_length=MAX_POSTING_TITLE_LENGTH)
    body: str = Field(min_length=1)
    is_locked: bool
    password: Optional[str] = None
    
    @validator('password', always=True)
    def validate_is_locked_password(
        cls, password: Optional[str], values: Dict[str, Optional[str]]):
        is_locked: bool = values.get('is_locked')
        if is_locked and (password is None):
            raise ValueError('set password if is_locked True')
        return password
    
    class Config():
        schema_extra = {
            "title" : "땃쥐의 유해성",
            "body" : "<p>땃쥐를 보면 심장에 무리가 가므로 장시간의 관찰은 자제해야한다.</p>",
            "is_locked" : False,
            "password" : "notyethashed"
        }
        

class PostingSchemasBaseModel(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=MAX_POSTING_TITLE_LENGTH)
    published_at: int
    updated_at: int
    is_locked: bool
    
    class Config():
        orm_mode = True
        schema_extra = {
            "id" : 13,
            "title" : "13번째 포스팅",
            "published_at" : 1672791019,
            "updated_at" : 1672791019,
            "is_locked" : False,
        }

class ResponsePostingPreview(PostingSchemasBaseModel):
    comment_comunt: Optional[int]
    creator: Optional[user_schemas.ResponseUserPreview]
    own_community: Optional[community_schemas.ResponseCommunitySchemasBaseModel]

    class Config():
        schema_extra = {
            "id" : 13,
            "title" : "13번째 포스팅",
            "published_at" : 1672791019,
            "updated_at" : 1672791019,
            "is_locked" : False,
            "comment_count" : 12,
            "creator" : user_schemas.ResponseUserPreview.Config.schema_extra,
            "own_community" : None
        }


class ResponsePostingDetail(PostingSchemasBaseModel):
    body: str = Field(min_length=1)
    comment_comunt: Optional[int]
    creator: Optional[user_schemas.ResponseUserPreview]
    # belongs_community: Optional[community_schemas.ResponseCommunitySchemasBaseModel]
    own_community: Optional[community_schemas.ResponseCommunitySchemasBaseModel]
    
    class Config():
        schema_extra = {
            "id" : 13,
            "title" : "13번째 포스팅",
            "body" : "<p>냥무</p>",
            "published_at" : 1672791019,
            "updated_at" : 1672791019,
            "is_locked" : False,
            "comment_count" : 12,
            "creator" : user_schemas.ResponseUserPreview.Config.schema_extra,
            "own_community" : None
        }
