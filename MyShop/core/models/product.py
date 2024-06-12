from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]


    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
