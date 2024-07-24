from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    shortname: str
    type: str
    battery: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    shortname: str | None = None
    type: str | None = None
    battery: str | None = None


class ProductRead(ProductBase):
    id: UUID
