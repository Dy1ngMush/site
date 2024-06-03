from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.products import crud
from core.models import db_helper, Product


async def product_by_id(
    product_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
