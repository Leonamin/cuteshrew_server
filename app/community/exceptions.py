from fastapi import HTTPException, status


def CommunityNotFound():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Community not found")


def UnauthorizedException():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Your don't have permission")
