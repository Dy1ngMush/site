from typing import Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.profile.schemas import ProfileCreate, ProfileRead, ProfileUpdatePartial
from core.models import Profile, User


async def create_profile(
    session: AsyncSession,
    profile_in: ProfileCreate,
) -> Profile:
    profile = Profile(**profile_in.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def get_profile(
    session: AsyncSession,
    user_id: UUID,
) -> Profile | None:
    return await session.scalar(select(Profile).where(Profile.user_id == user_id))


async def delete_profile(
    session: AsyncSession,
    profile: Profile,
) -> None:
    await session.delete(profile)
    await session.commit()


async def get_profile_by_user_id(
    session: AsyncSession,
    profile_id: UUID,
) -> Profile | None:
    return await session.scalar(select(Profile).where(Profile.id == profile_id))


async def update_profile(
    session: AsyncSession,
    profile: Profile,
    profile_update: ProfileUpdatePartial,
) -> Profile:
    for name, value in profile_update.model_dump(exclude_unset=True).items():
        setattr(profile, name, value)
    await session.commit()
    return profile
