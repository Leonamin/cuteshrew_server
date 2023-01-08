from typing import List, Optional
from pydantic import BaseModel

from app.dependency import Authority
from app.posting import schemas as posting_schemas

class ResponseCommunitySchemasBaseModel(BaseModel):
    id: Optional[int] = None
    name: str
    showname: str
    authority: Optional[Authority] = None
    created_at: Optional[int] = None
    published_at: Optional[int] = None
    posting_count: Optional[int] = None
    
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
            }
        }


class ReqeustCommunityCreate(BaseModel):
    name: str
    showname: str
    authority: Authority

    class Config:
        schema_extra = {
            "example": {
                "name": "general",
                "showname": "자유게시판",
                "authority": 9,
            }
        }

class ResponseCommunityInfo(ResponseCommunitySchemasBaseModel):
    id: Optional[int] = None
    name: str
    showname: str
    authority: Optional[Authority] = None
    created_at: Optional[int] = None
    published_at: Optional[int] = None
    posting_count: Optional[int] = None
    
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
            }
        }
        
        
class ResponseMainCommunityInfo(ResponseCommunityInfo):
    latest_postings: List[posting_schemas.PostingSchemasBaseModel]
    
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
                "postings" : [posting_schemas.PostingSchemasBaseModel.Config.schema_extra],           
            }
        }

class ResponseCommunityPageInfo(ResponseCommunityInfo):
    page_postings: List[posting_schemas.PostingSchemasBaseModel]
    
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
                "postings" : [posting_schemas.PostingSchemasBaseModel.Config.schema_extra],           
            }
        }