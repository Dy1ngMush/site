from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .token import Token
    from .profile import Profile
    from .order import Order
    from .trueorder import TrueOrder


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=False)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(String(5), default='true')
    role: Mapped[str] = mapped_column(String(32), default='regular')

    order: Mapped["Order"] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")
    token: Mapped["Token"] = relationship(back_populates="user")
    trueorder: Mapped["TrueOrder"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
