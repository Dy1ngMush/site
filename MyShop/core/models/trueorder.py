from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .trueorder_product_association import TrueOrderProductAssociation


class TrueOrder(UserRelationMixin, Base):
    _user_id_unique = False
    _user_back_populates = "trueorder"

    promocode: Mapped[str] = mapped_column(String(32), nullable=True)
    total_price: Mapped[int]

    products_details: Mapped[list["TrueOrderProductAssociation"]] = relationship(
        back_populates="trueorder"
    )