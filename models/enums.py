import enum


class RoleType(enum.Enum):
    approver:str = "approver"
    seller:str = "seller"
    buyer:str = "buyer"
    admin:str = "admin"
    

class ItemState(enum.Enum):
    pendding:str = "pendding"
    approved:str = "approved"
    rejected:str = "rejected"
