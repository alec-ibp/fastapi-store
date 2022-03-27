from pydantic import BaseModel, EmailStr


class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    phone: str
    iban: str
