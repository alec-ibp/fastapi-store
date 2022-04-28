from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    

class ItemBase(BaseModel):
    title: str
    description: str
    amount: float