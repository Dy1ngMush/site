from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.users import crud
from core.models import db_helper, User


async def user_by_id(
    user_id: Annotated[UUID, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {user} not found!",
    )
