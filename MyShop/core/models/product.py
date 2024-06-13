from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation
    from .trueorder_product_association import TrueOrderProductAssociation


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )

    true_orders_details: Mapped[list["TrueOrderProductAssociation"]] = relationship(
        back_populates="product",
    )
