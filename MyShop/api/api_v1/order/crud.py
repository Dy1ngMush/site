from pathlib import Path
from typing import Annotated
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1.order.schemas import OrderCreate
from api.api_v1.products.crud import get_product
from core.models import OrderProductAssociation, Order, Product


async def get_order_with_products_assoc(session: AsyncSession, order_id: UUID) -> Order:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .where(Order.id == order_id)
    )
    order = await session.scalar(stmt)
    return order


async def get_orders_with_products_assoc(session: AsyncSession, user_id) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .where(Order.user_id == user_id)
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def get_orders_with_products_with_associations(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)

    for order in orders:
        print(order.id, order.promocode, "products:")
        for (
            order_product_details
        ) in order.products_details:  # type: OrderProductAssociation
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.price,
                "quantity:",
                order_product_details.quantity,
            )


async def create_order(
    session: AsyncSession,
    order_in: OrderCreate,
) -> Order:
    order = Order(**order_in.model_dump())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def add_product_to_order(
    session: AsyncSession,
    order_id: UUID,
    product_id: UUID,
    quantity: int,
) -> Order:
    order = await session.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
    )
    product = await get_product(session, product_id)
    order.products_details.append(
        OrderProductAssociation(product=product, quantity=quantity)
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_order(
    session: AsyncSession,
    order_id: UUID,
) -> Order | None:
    return await session.get(Order, order_id)


async def get_order_product_associations(
    session: AsyncSession,
    order_id: UUID,
) -> list[OrderProductAssociation] | None:
    stmt = select(OrderProductAssociation).where(
        OrderProductAssociation.order_id == order_id
    )
    result = await session.scalars(stmt)
    return list(result)


async def get_order_one_product_associations(
    session: AsyncSession,
    order_id: UUID,
) -> OrderProductAssociation | None:
    stmt = select(OrderProductAssociation).where(
        OrderProductAssociation.order_id == order_id
    )
    result = await session.scalar(stmt)
    return result


async def delete_order(
    session: AsyncSession,
    order: Order,
) -> None:
    await session.delete(order)
    await session.commit()


async def delete_all_products_product_association(
    session: AsyncSession,
    order_product_association: list[OrderProductAssociation],
) -> None:
    for order_product_association in order_product_association:
        await session.delete(order_product_association)
    await session.commit()


async def delete_one_product_product_association(
    session: AsyncSession,
    order_product_association: OrderProductAssociation,
) -> None:
    await session.delete(order_product_association)
    await session.commit()
