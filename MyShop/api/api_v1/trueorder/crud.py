import uuid
from pathlib import Path
from typing import Annotated
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1.order.crud import delete_all_products_product_association
from api.api_v1.order.schemas import OrderCreate
from api.api_v1.products.crud import get_product
from core.models import (
    OrderProductAssociation,
    Order,
    Product,
    User,
    TrueOrder,
    TrueOrderProductAssociation,
)


async def create_order(
    access_token: UUID, session: AsyncSession, promocode: str | None
):
    user = select(User).where(User.id == access_token).options(selectinload(User.order))
    user = await session.scalar(user)
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .where(Order.id == user.order.id)
    )
    order = await session.scalar(stmt)
    total_price = 0
    for i in order.products_details:
        total_price += i.product.price * i.quantity
        print(i.product.id, i.product.price, i.quantity)
    idz = uuid.uuid4()
    session.add(
        TrueOrder(
            promocode=promocode,
            total_price=total_price,
            user_id=user.id,
            id=idz,
        )
    )
    await session.commit()
    for i in order.products_details:
        session.add(
            TrueOrderProductAssociation(
                true_order_id=idz,
                product_id=i.product.id,
                quantity=i.quantity,
            )
        )
        await session.commit()
    await delete_all_products_product_association(session, access_token)
    return f"Order created successfully ID: {idz}"


async def get_order(
    access_token: UUID,
    session: AsyncSession,
    order_id: UUID,
) -> TrueOrder:
    stmt = (
        select(TrueOrder)
        .options(
            selectinload(TrueOrder.products_details).joinedload(
                TrueOrderProductAssociation.product
            ),
        )
        .where(TrueOrder.id == order_id, TrueOrder.user_id == access_token)
    )
    result = await session.scalar(stmt)
    return result


async def delete_order(
    session: AsyncSession,
    order_id: UUID,
) -> None:
    trueorder = select(TrueOrder).where(TrueOrder.id == order_id)
    trueorder = await session.scalar(trueorder)
    await session.delete(trueorder)
    await session.commit()


async def delete_all_products_trueorders_product_association(
    session: AsyncSession, order_id: UUID
) -> None:
    stmt = (
        select(TrueOrderProductAssociation)
        .where(
            TrueOrderProductAssociation.true_order_id == order_id,
        )
        .order_by(TrueOrderProductAssociation.id)
    )
    true_order_product_associations = list(await session.scalars(stmt))
    for true_order_product_association in true_order_product_associations:
        await session.delete(true_order_product_association)
    await session.commit()
