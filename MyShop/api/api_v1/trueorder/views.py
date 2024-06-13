from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, Path
from sqlalchemy import select

from auth.utils import decode_jwt

from core.models import db_helper, TrueOrder
from secure import apikey_scheme
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Orders"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    promocode: str | None = None,
):
    access_token = decode_jwt(access_token)["sub"]
    return await crud.create_order(access_token, session, promocode)


@router.get("", response_model=None)
async def get_order(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_id: Annotated[UUID, Path],
):
    access_token = decode_jwt(access_token)["sub"]
    return await crud.get_order(access_token, session, order_id=order_id)


@router.delete("/delete_all_products", response_model=None)
async def delete_all_products_in_order(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_id: Annotated[UUID, Path],
):
    access_token = decode_jwt(access_token)["sub"]
    stmt = select(TrueOrder).where(
        TrueOrder.user_id == access_token, TrueOrder.id == order_id
    )
    result = await session.scalar(stmt)
    if result is not None:
        await crud.delete_all_products_trueorders_product_association(
            session=session, order_id=order_id
        )


@router.delete("/delete_order", response_model=None)
async def delete_order(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_id: Annotated[UUID, Path],
):
    access_token = decode_jwt(access_token)["sub"]
    stmt = select(TrueOrder).where(
        TrueOrder.user_id == access_token, TrueOrder.id == order_id
    )
    result = await session.scalar(stmt)
    if result is not None:
        return await crud.delete_order(session=session, order_id=order_id)
