from fastapi import APIRouter, status

from managers.user import UserManager
from schemas.request.user import UserLoginIn, UserRegisterIn


router = APIRouter(tags=["Authentication"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserRegisterIn) -> str:
    token: str = await UserManager.register(user_data.dict())
    return {"token": token}


@ router.post(
    path="/login",
    status_code=status.HTTP_200_OK
)
async def login(user_data: UserLoginIn) -> str:
    token: str = await UserManager.login(user_data.dict())
    return {"token": token}
