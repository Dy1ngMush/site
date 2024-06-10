from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Token(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "token"

    access_token: Mapped[str] = mapped_column(unique=True)
