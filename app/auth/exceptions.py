from fastapi import HTTPException, status


# def InvalidCredentials():
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                          detail=f"Invaild Credentials")


class InvalidCredentials(HTTPException):
    def __init(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials",
        self.headers = {"WWW-Authenticate": "Bearer"},


class IncorrectPassword(HTTPException):
    def __init(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Incorrect Password",
