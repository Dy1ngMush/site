from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: bytes
    active: bool = True


class UserToken(UserCreate):
    id: UUID


class UserUpdatePartial(UserCreate):
    username: str | None = None
    email: str | None = None
    password: bytes | None = None


class UserRead(UserBase):
    id: UUID


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str = None
