import time
from fastapi import APIRouter, Depends
from app.agora.dependencies import valid_time_limit, valid_role
from app.dependency import get_agora_app_id, get_agora_certificate
from agora_token_builder import RtcTokenBuilder

router = APIRouter(
    prefix="/agora",
    tags=['agora']
)


@router.get('/rtc')
def new_rtc():
    return {"channelName": "hiyo"}


@router.get('/rtc/{channel_name}/{role}/{uid}')
def join_session(
    channel_name: str,
    uid: int,
    role: int = Depends(valid_role),
    time_limit: int = Depends(valid_time_limit),
    app_id: str = Depends(get_agora_app_id),
    certificate: str = Depends(get_agora_certificate)
):
    privilegeExpiredTs = time.time() + time_limit * 60
    agora_token = RtcTokenBuilder.buildTokenWithUid(
        app_id, certificate, channel_name, uid, role, privilegeExpiredTs)
    return {"token": agora_token}
