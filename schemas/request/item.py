from schemas.base import ItemBase


class ItemIn(ItemBase):
    encoded_photo: str
    extension: str
    