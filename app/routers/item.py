from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

from app.routers.cart import find_cart_by_id

router = APIRouter(prefix="/carts/{id}/items", tags=["Items"])


class CartItem(BaseModel):
    name: str
    price: float = 0
    url: Optional[str]
    image_url: Optional[str]
    amount: Optional[int] = 1


@router.get("/")
def get_all_cart_items(id: str):
    cart = find_cart_by_id(id)

    return cart.get("items", [])


@router.get("/{item_id}")
def get_cart_item(id: str, item_id: str):
    cart = find_cart_by_id(id)
    item = find_cart_item_by_id(cart, item_id)

    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cart_item(id: str, item: CartItem):
    cart = find_cart_by_id(id)
    item_dict = item.dict()

    item_dict["_id"] = str(uuid4())

    cart["items"].append(item_dict)

    return item_dict


@router.patch("/{item_id}")
def update_cart_item(id: str, item_id: str, cart_item: CartItem):
    cart = find_cart_by_id(id)
    item = find_cart_item_by_id(cart, item_id)

    for value in cart_item:
        if value[1]:
            item[value[0]] = value[1]

    return cart


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(id: str, item_id: str):
    cart = find_cart_by_id(id)
    item = find_cart_item_by_id(cart, item_id)

    cart["items"].remove(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def find_cart_item_by_id(cart, id):
    for item in cart["items"]:
        if item["_id"] == id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"cart item with id {id} was not found",
    )
