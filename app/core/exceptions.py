from fastapi import HTTPException, status


def DuplicateEmailException():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="이미 등록된 이메일입니다.")


def InvalidCredentialsException():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="잘못된 이메일 또는 비밀번호입니다.")


def UserNotFoundException():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 유저입니다.",
    )