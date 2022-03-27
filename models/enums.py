import enum


class RoleType(enum.Enum):
    approver = "approver"
    seller = "seller"
    buyer = "buyer"
    admin = "admin"
    