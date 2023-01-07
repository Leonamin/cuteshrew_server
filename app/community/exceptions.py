from fastapi import HTTPException, status


def CommunityNotFound():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Community not found")


def UnauthorizedException():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Your don't have permission")


def InvalidLoadCountException():
    return HTTPException(status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
                         detail="Load count must be less than 100 or over than 0")


def InvalidCommunityName():
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail="/info /page /all is not valid name for community")
