from fastapi import HTTPException, status


def PostingNotFound():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Posting not found")


def UnauthorizedException():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Your don't have permission")


def InvalidLoadCountException():
    return HTTPException(status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
                         detail="Load count must be less than 100 or over than 0")


def NeedPasswordException():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="You must send password")


def InvalidPasswordException():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Invalid password")


def InvalidPageNum():
    return HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                         detail="Invalid page num")
