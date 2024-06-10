from typing import Annotated

from fastapi import APIRouter, status, Depends

from auth.utils import decode_jwt
from core.models import db_helper, Profile
from secure import apikey_scheme
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import profile_by_id
from .schemas import ProfileCreate, ProfileRead, ProfileUpdate, ProfileUpdatePartial

router = APIRouter(tags=["Profiles"])


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    profile_in: ProfileCreate,
):
    access_token = decode_jwt(access_token)
    profile_in.user_id = access_token["sub"]
    return await crud.create_profile(session=session, profile_in=profile_in)


@router.get("", response_model=ProfileRead)
async def get_profile(
    profile: Profile = Depends(profile_by_id),
):
    return profile


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    access_token: Annotated[str, Depends(apikey_scheme)],
    profile: Profile = Depends(profile_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud.delete_profile(
        session=session,
        profile=profile,
    )
