from typing import Dict, List

from fastapi import HTTPException, status
from asyncpg import UniqueViolationError
from passlib.context import CryptContext

from db.init_db import database
from managers.auth import AuthManager
from models import user
from schemas.response.user import UserOut


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data: Dict) -> str:
        user_data["password"] = pwd_context.hash(user_data["password"])

        try:
            id_ = await database.execute(user.insert().values(user_data))
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User email already exists!")
        
        user_db: Dict = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_db)        

    @staticmethod
    async def login(user_data: Dict) -> str:
        user_db = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))

        if not user_db or not pwd_context.verify(user_data["password"], user_db["password"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email or password")

        return AuthManager.encode_token(user_db)

    @staticmethod
    async def get_all() ->List[UserOut]:
        return await database.fetch_all(user.select())
        