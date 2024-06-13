from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .trueorder import TrueOrder
    from .product import Product


class TrueOrderProductAssociation(Base):
    __tablename__ = "true_order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "true_order_id",
            "product_id",
            name="idx_unique_true_order_product",
        ),
    )

    true_order_id: Mapped[int] = mapped_column(ForeignKey("true_orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")

    trueorder: Mapped["TrueOrder"] = relationship(back_populates="products_details")

    product: Mapped["Product"] = relationship(back_populates="true_orders_details")
