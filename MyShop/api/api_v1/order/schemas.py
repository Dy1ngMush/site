from uuid import UUID

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: UUID


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: UUID


class OrderUpdate(OrderBase):
    pass
