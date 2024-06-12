from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.demo_auth.helpers import create_access_token
from auth.utils import validate_password
from core.models import Token, User
from api.api_v1.users.schemas import UserCreate


async def create_token(session: AsyncSession, user_data: UserCreate) -> Token:
    query = select(User).where(User.email == user_data.email)
    user: User = await session.scalar(query)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not validate_password(user_data.password.decode(), user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password",
        )
    token: Token = Token(user_id=user.id, access_token=create_access_token(user))
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return Token(
        access_token=token.access_token,
    )


async def get_token(
    session: AsyncSession,
    token_id: UUID,
) -> Token | None:
    return await session.get(Token, token_id)


async def get_token_by_user_id(
    session: AsyncSession,
    user_id: UUID,
) -> Token | None:
    return await session.scalar(select(Token).where(Token.user_id == user_id))


async def delete_token(session: AsyncSession, token: Token) -> None:
    await session.delete(token)
    await session.commit()
