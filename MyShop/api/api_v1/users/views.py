from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .schemas import UserRead, UserCreate
from . import crud as users_crud

router = APIRouter(tags=["Users"])


@router.get("", response_model=list[UserRead])
async def get_users(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    users = await users_crud.get_all_users(session=session)
    return users

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user: UserRead = Depends(user_by_id),
):
    return user

@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_create: UserCreate,
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_partial(
    user_update_partial: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update_partial,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud.delete_user(
        session=session,
        user=user,
    )
