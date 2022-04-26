from typing import List

from fastapi import APIRouter, Depends, status

from managers.user import UserManager
from managers.auth import oauth2_scheme
from schemas.response.user import UserOut


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserOut],
    dependencies=[Depends(oauth2_scheme)]
)
async def get_users():
    return await UserManager.get_all()
