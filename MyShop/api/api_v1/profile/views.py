from typing import Annotated
from typing import Annotated, Any

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select

from auth.utils import decode_jwt
from core.models import db_helper, Profile, User
from secure import apikey_scheme
from . import crud
from api.api_v1.users import crud as crud_user
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import profile_by_id, profile_by_profile_id
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

@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_user_partial(
    access_token: Annotated[str, Depends(apikey_scheme)],
    profile_update_partial: ProfileUpdatePartial,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    access_token = decode_jwt(access_token)["sub"]
    profile = await crud.get_profile(session=session, user_id=access_token)
    return await crud.update_profile(
        session=session,
        profile=profile,
        profile_update=profile_update_partial,
    )
