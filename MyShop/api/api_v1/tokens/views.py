from typing import Annotated

from fastapi import APIRouter, status, Depends
from core.models import db_helper
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import token_by_id
from .schemas import Token, TokenRead
from ..users.schemas import UserCreate

router = APIRouter(tags=["Tokens"])


@router.post("", response_model=TokenRead, status_code=status.HTTP_201_CREATED)
async def create_token(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.create_token(session=session, user_data=user_data)


@router.delete("/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token(
    token: Token = Depends(token_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud.delete_token(
        session=session,
        token=token,
    )
