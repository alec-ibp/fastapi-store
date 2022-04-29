from typing import List

from fastapi import APIRouter, Depends, status

from managers.user import UserManager
from managers.auth import is_admin, oauth2_scheme
from models.enums import RoleType
from schemas.response.user import UserOut


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserOut],
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)]
)
async def get_users():
    return await UserManager.get_all()


@router.put(
    path="/{user_id}/make-admin",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)]
)
async def make_admin(user_id: int):
    await UserManager.change_roll(user_id, RoleType.admin)


@router.put(
    path="/{user_id}/make-seller",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)]
)
async def make_admin(user_id: int):
    await UserManager.change_roll(user_id, RoleType.seller)
