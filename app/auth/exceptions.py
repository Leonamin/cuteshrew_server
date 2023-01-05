from fastapi import HTTPException, status

def InvalidCredentials():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Invaild Credentials")