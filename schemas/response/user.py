from schemas.base import UserBase


class UserOut(UserBase):
    firstname: str
    lastname: str
    phone: str
    