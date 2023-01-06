from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/general')
def create_user():
    pass


@router.post('/admin')
def create_user_for_admin():
    pass


@router.get('/search')
def get_user():
    pass
