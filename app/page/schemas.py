from typing import List

from app.community import schemas as community_schemas
from app.posting import schemas as posting_schemas

class ResponsePostingPage(posting_schemas.PostingSchemasBaseModel):
    comment_count: int
    
    class Config():
        orm_mode = True
        schema_extra = {
            "id" : 13,
            "title" : "13번째 포스팅",
            "published_at" : 1672791019,
            "updated_at" : 1672791019,
            "is_locked" : False,
            "comment_count": int
        }

class ResponseMainPage(community_schemas.ResponseCommunityInfo):
    latest_postings: List[ResponsePostingPage]
    
    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "general",
                "showname": "자유게시판",
                "authority": 9,
                "created_at": 1672791019,
                "published_at" : 1672794023,
                "posting_count": 123,  
                "postings" : [ResponsePostingPage.Config.schema_extra],           
            }
        }

class ResponseCommunityPage(community_schemas.ResponseCommunityInfo):
    page_postings: List[ResponsePostingPage]
    
    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "general",
                "showname": "자유게시판",
                "authority": 9,
                "created_at": 1672791019,
                "published_at" : 1672794023,
                "posting_count": 123,  
                "postings" : [ResponsePostingPage.Config.schema_extra],           
            }
        }