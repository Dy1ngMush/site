from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.profile import crud
from core.models import db_helper, Profile


async def profile_by_id(
    profile_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Profile:
    print(profile_id)
    profile = await crud.get_profile(session=session, user_id=profile_id)
    if profile is not None:
        return profile
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Profile not found!",
    )
