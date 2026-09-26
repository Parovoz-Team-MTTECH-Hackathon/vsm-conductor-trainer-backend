from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Management(Base):
    __tablename__ = "managements"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.client_id"), primary_key=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.client_id"), primary_key=True)