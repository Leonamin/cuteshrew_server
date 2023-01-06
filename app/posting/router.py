from fastapi import APIRouter, Depends, status


router = APIRouter(
    prefix="/community/{name}",
    tags=['posting']
)


@router.get("/{id}", response_model_exclude_none=True)
def get_post():
    pass


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post():
    pass


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post():
    pass


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post():
    pass
