from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, Path

from auth.utils import decode_jwt

from core.models import db_helper
from secure import apikey_scheme
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import OrderRead, OrderCreate

router = APIRouter(tags=["Carts"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_cart(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_in: OrderCreate,
):
    access_token = decode_jwt(access_token)["sub"]
    order_in.user_id = access_token
    return await crud.create_order(session=session, order_in=order_in)


@router.get("", response_model=None)
async def get_cart(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    access_token = decode_jwt(access_token)["sub"]
    return await crud.get_orders_with_products_assoc(
        session=session, user_id=access_token
    )


@router.post("/add_product", response_model=OrderRead)
async def add_product_to_cart(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_id: Annotated[UUID, Path],
    quantity: int,
):
    access_token = decode_jwt(access_token)["sub"]
    return await crud.add_product_to_order(
        session=session,
        access_token=access_token,
        product_id=product_id,
        quantity=quantity,
    )


@router.delete("/delete_all_products", response_model=None)
async def delete_all_products_in_cart(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    access_token = decode_jwt(access_token)["sub"]
    await crud.delete_all_products_product_association(
        session=session,
        access_token=access_token,
    )


@router.delete("/delete_one_product/{product_id}", response_model=None)
async def delete_one_product_in_cart(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_id: Annotated[UUID, Path],
):
    access_token = decode_jwt(access_token)["sub"]
    await crud.delete_one_product_product_association(
        session=session,
        access_token=access_token,
        product_id=product_id,
    )


@router.delete("/delete_cart", response_model=None)
async def delete_cart(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    access_token = decode_jwt(access_token)["sub"]
    return await crud.delete_order(session=session, access_token=access_token)
