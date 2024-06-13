from typing import Annotated

from fastapi import APIRouter, status, Depends
from .dependencies import product_by_id
from core.models import db_helper, Product
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ProductCreate, ProductRead, ProductUpdate, ProductUpdatePartial

router = APIRouter(tags=["Products"])


@router.get("", response_model=list[ProductRead])
async def get_all_products(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.get_products(session=session)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_in: ProductCreate,
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product: ProductRead = Depends(product_by_id),
):
    return product


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product_partial(
    product_update_partial: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update_partial,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud.delete_product(
        session=session,
        product=product,
    )
