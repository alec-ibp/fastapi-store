from datetime import datetime

from schemas.base import ItemBase
from models import ItemState


class ItemsOut(ItemBase):
    id: int
    photo_url: str
    created_at: datetime
    status: ItemState
