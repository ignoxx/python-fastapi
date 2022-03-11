from lib2to3.pytree import Base
from typing import Dict
from fastapi import FastAPI, APIRouter, HTTPException, Response, status
from app.database import db
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter(prefix="/carts", tags=["Carts"])


class Cart(BaseModel):
    name: str
    public: bool = False
    url: Optional[str]
    image_url: Optional[str]
    items: Optional[list] = []


class UpdateCart(BaseModel):
    name: str
    public: Optional[bool]
    image_url: Optional[str]


@router.get("/")
def get_all_carts():
    return db


@router.get("/{id}")
def get_cart(id: str):
    cart = find_cart_by_id(id)
    return cart


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cart(cart: Cart):
    cart_dict = cart.dict()
    cart_dict["_id"] = str(uuid4())

    db.append(cart_dict)

    return cart_dict


@router.patch("/{id}")
def update_cart(id: str, cart: UpdateCart):
    existing_cart = find_cart_by_id(id)

    for value in cart:
        if value[1]:
            existing_cart[value[0]] = value[1]

    return existing_cart


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id: str):
    cart = find_cart_by_id(id)

    db.remove(cart)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def find_cart_by_id(id):
    for cart in db:
        if cart["_id"] == id:
            return cart

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"cart with id {id} was not found",
    )
