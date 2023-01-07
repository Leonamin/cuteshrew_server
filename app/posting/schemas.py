from typing import Optional
from pydantic import BaseModel, Field

from app.posting.constants import MAX_POSTING_TITLE_LENGTH
from app.user import schemas as user_schemas

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
    # own_community: Optional[None]

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
    body: str
    comment_comunt: Optional[int]
    creator: Optional[user_schemas.ResponseUserPreview]
    # own_community: Optional[None]
    
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
