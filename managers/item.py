import os
import uuid
from typing import Dict, List

from fastapi import HTTPException, status

from db.init_db import database
from models import item
from models.enums import ItemState, RoleType
from schemas.request.item import ItemIn
from schemas.response.item import ItemsOut
from services.store_static_files_s3 import S3Service
from constants import TEMP_FILE_FOLDER
from utils.helpers import decode_photo


s3 = S3Service()

class ItemManager:
    @staticmethod
    async def __get_item(item_id: int) -> bool:
        item_db = await database.fetch_one(item.select().where(item.c.id == item_id))
        if item_db != None:
            return True
        return False

    @staticmethod
    async def create(item_data: ItemIn, user: Dict) -> ItemsOut:
        item_data["seller_id"] = user["id"]
        encoded_photo = item_data.pop("encoded_photo")
        extension = item_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        item_data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)

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
    async def get_items(user: Dict) -> List[ItemsOut]:
        id = user["id"]
        query = item.select()
        if user["role"] == RoleType.seller:
            query = item.select().where(item.c.seller_id == id)
        return await database.fetch_all(query)
        
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
