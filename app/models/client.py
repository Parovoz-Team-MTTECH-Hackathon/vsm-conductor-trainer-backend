import enum
from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class ClientType(enum.StrEnum):
    USER = "user"
    INTEGRATION = "integration"


class UserType(enum.StrEnum):
    PLAYER = "player"
    ADMIN = "admin"
    MANAGER = "manager"


class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    client_type: Mapped[ClientType] = mapped_column(Enum(ClientType, name="client_type"), nullable=False)

    __mapper_args__ = dict(polymorphic_on=client_type)


class Integration(Client):
    __tablename__ = "integrations"

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id", ondelete="CASCADE"), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    secret_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    __mapper_args__ = dict(polymorphic_identity=ClientType.INTEGRATION)


class User(Client):
    __tablename__ = "users"

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id", ondelete="CASCADE"), primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name="user_type"), nullable=False)

    __mapper_args__ = dict(polymorphic_identity=ClientType.USER, polymorphic_on=user_type)


class Admin(User):
    __mapper_args__ = dict(polymorphic_identity=UserType.ADMIN)


class Player(User):
    __tablename__ = "players"

    client_id: Mapped[int] = mapped_column(ForeignKey("users.client_id", ondelete="CASCADE"), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    patronymic_name: Mapped[str] = mapped_column(String(64), nullable=False)

    __mapper_args__ = dict(polymorphic_identity=UserType.PLAYER)


class Manager(User):
    __tablename__ = "managers"

    client_id: Mapped[int] = mapped_column(ForeignKey("users.client_id", ondelete="CASCADE"), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    __mapper_args__ = dict(polymorphic_identity=UserType.MANAGER)


class Management(Base):
    __tablename__ = "managements"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.client_id", ondelete="CASCADE"), primary_key=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.client_id", ondelete="CASCADE"), primary_key=True)