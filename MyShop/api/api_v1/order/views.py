from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, status, Depends, Path
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from auth.utils import decode_jwt
from core.models import OrderProductAssociation, Product
from core.models import db_helper, Order
from secure import apikey_scheme
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import (
    order_by_id,
    order_product_associations_by_id,
    order_one_product_associations_by_id,
)
from .schemas import OrderBase, OrderRead, OrderCreate
from ..products.schemas import ProductRead

router = APIRouter(tags=["Orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_in: OrderCreate,
):
    access_token = decode_jwt(access_token)["sub"]
    order_in.user_id = access_token
    return await crud.create_order(session=session, order_in=order_in)


@router.get("", response_model=List[OrderRead])
async def get_user_orders(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    access_token = decode_jwt(access_token)["sub"]
    return await crud.get_orders_with_products_assoc(
        session=session, user_id=access_token
    )


@router.get("/{order_id}", response_model=None)
async def get_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order: Annotated[UUID, Path],
):
    return await crud.get_order_with_products_assoc(session=session, order_id=order)


@router.post("/add_product/{order_id}", response_model=OrderRead)
async def add_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order: Annotated[UUID, Path],
    product_id: Annotated[UUID, Path],
    quantity: int,
):
    return await crud.add_product_to_order(
        session=session,
        order_id=order,
        product_id=product_id,
        quantity=quantity,
    )


@router.delete("/delete_all_products/{order_id}", response_model=None)
async def delete_all_products(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_product_associations: list[OrderProductAssociation] = Depends(
        order_product_associations_by_id
    ),
):
    await crud.delete_all_products_product_association(
        session=session, order_product_association=order_product_associations
    )


@router.delete("/delete_one_product/{order_id}", response_model=None)
async def delete_one_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_product_associations: OrderProductAssociation = Depends(
        order_one_product_associations_by_id
    ),
):
    await crud.delete_one_product_product_association(
        session=session, order_product_association=order_product_associations
    )


@router.delete("/delete_order/{order_id}", response_model=None)
async def delete_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order: Order = Depends(order_by_id),
):
    return await crud.delete_order(session=session, order=order)


#    return await crud.get_order(session=session, order_id=order)


# orders = await crud.get_orders_with_products_assoc(session=session)
# for order in orders:
#     print(order.id, order.promocode, "products:")
#     for (
#         order_product_details
#     ) in order.products_details:  # type: OrderProductAssociation
#         print(
#             "-",
#             order_product_details.product.name,
#             order_product_details.product.price,
#             "quantity:",
#             order_product_details.quantity,
#         )
