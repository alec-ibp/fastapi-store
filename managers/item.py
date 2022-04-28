from typing import Dict, List

from fastapi import HTTPException, status

from db.init_db import database
from models import item
from models.enums import ItemState
from schemas.request.item import ItemIn
from schemas.response.item import ItemsOut


class ItemManager:
    @staticmethod
    async def __get_item(item_id: int) -> bool:
        return await database.fetch_one(item.select().where(item.c.id == item_id))

    @staticmethod
    async def create(item_data: ItemIn, user: Dict) -> ItemsOut:
        item_data["seller_id"] = user["id"]
        _id = await database.execute(item.insert().values(item_data))
        return await database.fetch_one(item.select().where(item.c.id == _id))

    @staticmethod
    async def buy(item_id: int) -> None:
        if await ItemManager.__get_item(item_id):
            # TODO make transfer, confirm and delete sold item
            await database.execute(item.update().where(item.c.id == item_id).values(status=ItemState.approved))
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist!")

    @staticmethod
    async def get_all(user: Dict) -> List[ItemsOut]:
        id = user["id"]
        return await database.fetch_all(item.select().where(item.c.seller_id == id))
        
    @staticmethod
    async def approve(item_id: int) -> None:
        if await ItemManager.__get_item(item_id):
            await database.execute(item.update().where(item.c.id == item_id).values(status=ItemState.approved))
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist!")

    @staticmethod
    async def reject(item_id: int) -> None:
        if await ItemManager.__get_item(item_id):
            await database.execute(item.update().where(item.c.id == item_id).values(status=ItemState.rejected))
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist!")

    @staticmethod
    async def delete(item_id: int) -> None:
        if await ItemManager.__get_item(item_id):
            await database.execute(item.delete().where(item.c.id == item_id))
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist!")
