from typing import Optional
from pydantic import BaseModel

from app.user import schemas as user_schemas
from app.posting import schemas as posting_schemas


class ResponseCommentBaseModel(BaseModel):
    id: int
    user_id: int
    created_at: int
    post_id: int
    comment_class: Optional[int] = None
    order: Optional[int] = None
    group_id: Optional[int] = None

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 13,
                "user_id": 1,
                "created_at": 1672791019,
                "post_id": 12,
                "comment_class": 1,
                "order": 3,
                "group_id": 13
            },
            "reply": {
                "id": 16,
                "user_id": 1,
                "created_at": 1672791019,
                "post_id": 12,
                "comment_class": 2,
                "order": 1,
                "group_id": 13
            }
        }


class ResponseCommentPreview(ResponseCommentBaseModel):
    pass
    # creator: Optional[user_schemas.ResponseUserPreview] = None
    # posting: Optional[posting_schemas.ResponsePostingPreview] = None

    # class Config():
    #     schema_extra = {
    #         "comment": {
    #             "id": 13,
    #             "user_id": 1,
    #             "created_at": 1672791019,
    #             "post_id": 12,
    #             "comment_class": 1,
    #             "order": 3,
    #             "group_id": 13,
    #             "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
    #             "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra
    #         },
    #         "reply": {
    #             "id": 16,
    #             "user_id": 1,
    #             "created_at": 1672791019,
    #             "post_id": 12,
    #             "comment_class": 2,
    #             "order": 1,
    #             "group_id": 13,
    #             "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
    #             "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra

    #         }
    #     }


class ResponseCommentDetail(ResponseCommentBaseModel):
    comment: str
    # creator: Optional[user_schemas.ResponseUserPreview] = None
    # posting: Optional[posting_schemas.ResponsePostingPreview] = None

    class Config():
        schema_extra = {
            "example": {
                "id": 13,
                "comment": "Blessed are the peacemakers",
                "user_id": 1,
                "created_at": 1672791019,
                "post_id": 12,
                "comment_class": 1,
                "order": 3,
                "group_id": 13,
                # "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
                # "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra
            },
            "reply": {
                "id": 16,
                "comment": "Blessed are the peacemakers",
                "user_id": 1,
                "created_at": 1672791019,
                "post_id": 12,
                "comment_class": 2,
                "order": 1,
                "group_id": 13,
                # "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
                # "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra

            }
        }
