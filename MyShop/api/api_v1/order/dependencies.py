from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.order import crud
from core.models import db_helper, Order, OrderProductAssociation


async def order_by_id(
    order_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Order:
    order = await crud.get_order(session=session, order_id=order_id)
    if order is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found!",
    )


async def order_product_associations_by_id(
    order_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[OrderProductAssociation]:
    order = await crud.get_order_product_associations(
        session=session, order_id=order_id
    )
    if order is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found!",
    )


async def order_one_product_associations_by_id(
    order_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> OrderProductAssociation:
    order = await crud.get_order_one_product_associations(
        session=session, order_id=order_id
    )
    if order is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found!",
    )
