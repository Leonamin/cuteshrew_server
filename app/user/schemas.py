from pydantic import BaseModel, SecretStr


class RequestUserCreate(BaseModel):
    nickname: str
    email: str
    password: SecretStr
