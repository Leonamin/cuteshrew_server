from fastapi import APIRouter, Depends
from app.dependency import get_zoom_sdk_key, get_zoom_sdk_secret
from app.zoom.dependencies import create_session_token
from datetime import timedelta

router = APIRouter(
    prefix="/zoom",
    tags=['zoom']
)


@router.get('/session/{session_name}')
def join_session(
    session_name: str,
    secret_key: str = Depends(get_zoom_sdk_secret),
    zoom_sdk_key: str = Depends(get_zoom_sdk_key)
):
    session_token = create_session_token(
        data={
            "app_key": zoom_sdk_key,
            "tpc": session_name,
            "version": 1,
            "role_type": 0,
            "pwd": 12345
        },
        expires_delta=timedelta(seconds=2000),
        secret_key=secret_key,
    )

    return {"session_token": session_token}


@router.post('/session/{session_name}')
def host_session(
    session_name: str,
    secret_key: str = Depends(get_zoom_sdk_secret),
    zoom_sdk_key: str = Depends(get_zoom_sdk_key)
):
    session_token = create_session_token(
        data={
            "app_key": zoom_sdk_key,
            "tpc": session_name,
            "version": 1,
            "role_type": 1,
            "pwd": 12345
        },
        expires_delta=timedelta(seconds=2000),
        secret_key=secret_key,
    )

    return {"session_token": session_token}