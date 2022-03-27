from typing import List

from fastapi import APIRouter, status

from managers.user import UserManager
from schemas.response.user import UserOut


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserOut]
)
async def get_users():
    return await UserManager.get_all()