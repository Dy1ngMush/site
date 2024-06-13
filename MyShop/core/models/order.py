from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation


class Order(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "order"

    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
