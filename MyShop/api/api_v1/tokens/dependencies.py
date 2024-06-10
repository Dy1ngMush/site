from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.tokens import crud
from core.models import db_helper, Token


async def token_by_id(
    token_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Token:
    token = await crud.get_token(session=session, token_id=token_id)
    if token is not None:
        return token
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {token_id} not found!",
    )
