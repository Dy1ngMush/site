from uuid import UUID

from pydantic import BaseModel


class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: str


class ProfileCreate(ProfileBase):
    user_id: UUID


class ProfileUpdate(ProfileCreate):
    pass


class ProfileUpdatePartial(ProfileCreate):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


class ProfileRead(ProfileBase):
    id: UUID
    user_id: UUID
