from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

possible_roles = ['regular', 'admin', 'superadmin']

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = possible_roles[0]


class UserCreate(UserBase):
    password: bytes
    active: str = 'true'


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
