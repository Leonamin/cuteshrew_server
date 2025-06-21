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


def PostNotFoundException():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 게시글입니다.",
    )


def PostNotAuthorizedException():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="게시글 작성자가 아닙니다.",
    )