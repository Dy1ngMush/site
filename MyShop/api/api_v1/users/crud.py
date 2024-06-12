from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from core.models import Token
from core.models.user import User
from api.api_v1.users.schemas import UserCreate, UserUpdatePartial


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    if await session.scalar(select(User).where(User.email == user_create.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_create.email} already exists",
        )
    user_create.password = hash_password(user_create.password.decode()).decode()
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(
    session: AsyncSession,
    user_id: UUID,
) -> User | None:
    return await session.scalar(select(User).where(User.id == user_id))


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdatePartial,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
    token: Token,
) -> None:
    await session.delete(token)
    await session.delete(user)
    await session.commit()
