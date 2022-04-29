from typing import List

from fastapi import APIRouter, Depends, Request, status

from managers.item import ItemManager
from managers.auth import is_admin, is_buyer, oauth2_scheme, is_seller, is_approver
from schemas.request.item import ItemIn
from schemas.response.item import ItemsOut

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ItemsOut],
    dependencies=[Depends(oauth2_scheme)]
)
async def get_items(request: Request):
    user = request.state.user
    return await ItemManager.get_items(user)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemsOut,
    dependencies=[Depends(oauth2_scheme), Depends(is_seller)]
)
async def create_item(request: Request, item: ItemIn):
    user = request.state.user
    return await ItemManager.create(item.dict(), user)


@router.put(
    path="/{item_id}/shop",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(oauth2_scheme), Depends(is_buyer)]
)
async def buy_item(item_id: int):
    await ItemManager.buy(item_id)


@router.put(
    path="/{item_id}/approve",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)]
)
async def aprrove_item(item_id: int):
    await ItemManager.approve(item_id)


@router.put(
    path="/{item_id}/reject",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)]
)
async def reject_item(item_id: int):
    await ItemManager.reject(item_id)


@router.delete(
    path="/{item_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)]
)
async def delete_item(item_id: int):
    await ItemManager.delete(item_id)
