from typing import Optional
from app.user import schemas as user_schemas
from app.comment import schemas as comment_schemas
from app.posting import schemas as posting_schemas


class ResponseSearchPostingPreview(posting_schemas.ResponsePostingPreview):
    pass


class ResponseSearchCommentPreview(comment_schemas.ResponseCommentBaseModel):
    creator: Optional[user_schemas.ResponseUserPreview] = None
    posting: Optional[posting_schemas.ResponsePostingPreview] = None

    class Config():
        schema_extra = {
            "example": {
                "id": 13,
                "user_id": 1,
                "created_at": 1672791019,
                "post_id": 12,
                "comment_class": 1,
                "order": 3,
                "group_id": 13,
                "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
                "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra
            },
            "example_reply": {
                "id": 16,
                "user_id": 1,
                "created_at": 1672791019,
                "post_id": 12,
                "comment_class": 2,
                "order": 1,
                "group_id": 13,
                "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
                "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra
            }
        }


class ResponseSearchCommentDetail(comment_schemas.ResponseCommentBaseModel):
    comment: str
    creator: Optional[user_schemas.ResponseUserPreview] = None
    posting: Optional[posting_schemas.ResponsePostingPreview] = None

    class Config():
        schema_extra = {
            "example": {
                "id": 13,
                "user_id": 1,
                "created_at": 1672791019,
                "comment": "Call Me Ishmael",
                "post_id": 12,
                "comment_class": 1,
                "order": 3,
                "group_id": 13,
                "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
                "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra
            },
            "example_reply": {
                "id": 16,
                "user_id": 1,
                "created_at": 1672791019,
                "comment": "Call Me Ishmael",
                "post_id": 12,
                "comment_class": 2,
                "order": 1,
                "group_id": 13,
                "creator": user_schemas.ResponseUserPreview.Config.schema_extra,
                "posting": posting_schemas.ResponsePostingPreview.Config.schema_extra
            }
        }
