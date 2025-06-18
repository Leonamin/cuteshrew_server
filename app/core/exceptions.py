from fastapi import HTTPException, status


def DuplicateEmailException():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="이미 등록된 이메일입니다.")
