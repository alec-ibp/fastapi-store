from pydantic import EmailStr
from schemas.base import UserBase


class UserLoginIn(UserBase):
    password: str

class UserRegisterIn(UserLoginIn):
    firstname: str
    lastname: str
    phone: str
    iban: str
