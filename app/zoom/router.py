from fastapi import APIRouter, Depends
from app.dependency import get_secret_key, get_zoom_sdk_key
from app.zoom.dependencies import create_session_token
from datetime import timedelta

router = APIRouter(
    prefix="/zoom",
    tags=['zoom']
)


@router.get('/session')
def session(
    secret_key: str = Depends(get_secret_key),
    zoom_sdk_key: str = Depends(get_zoom_sdk_key)
):
    session_token = create_session_token(
        data={
            "app_key": zoom_sdk_key,
            "tpc": "functional_test",
            "version": 1,
            "role_type": 0,
            "pwd": 12345
        },
        expires_delta=timedelta(seconds=2000),
        secret_key=secret_key,
    )

    return {"session_token": session_token}
