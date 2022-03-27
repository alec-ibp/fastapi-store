from fastapi import APIRouter

from managers.user import UserManager
from schemas.request.user import UserRegisterIn


router = APIRouter(tags=["Authentication"])


@router.post("/register")
async def register(user_data: UserRegisterIn) -> str:
    token = await UserManager.register(user_data.dict())
    return {"token": token}
