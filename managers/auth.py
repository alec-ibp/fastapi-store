from typing import Dict
from datetime import datetime, timedelta

import jwt

from core.config import settings


class AuthManager:
    @staticmethod
    def encode_token(user: Dict) -> str:
        payload: Dict = {
            "sub": user["id"],
            "exp": datetime.utcnow() + timedelta(minutes=120)
        }
        
        try:
            return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        except Exception as ex:
            raise ex
