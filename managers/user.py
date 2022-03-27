from typing import Dict

from fastapi import HTTPException, status
from asyncpg import UniqueViolationError
from passlib.context import CryptContext

from db.init_db import database
from managers.auth import AuthManager
from models import user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data: Dict) -> str:
        user_data["password"] = pwd_context.hash(user_data["password"])

        try:
            id_ = await database.execute(user.insert().values(user_data))
        except UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User email already exists!")
        
        user_db: Dict = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_db)        
