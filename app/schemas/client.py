from pydantic import BaseModel, ConfigDict
from app.models import ClientType, UserType


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    client_id: int
    is_active: bool
    client_type: ClientType


class IntegrationResponse(ClientResponse):
    model_config = ConfigDict(from_attributes=True)
    name: str
    key: str


class UserResponse(ClientResponse):
    model_config = ConfigDict(from_attributes=True)
    email: str
    user_type: UserType


class AdminResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)


class PlayerResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    patronymic_name: str


class PublicPlayerResponse(ClientResponse):
    model_config = ConfigDict(from_attributes=True)
    user_type: UserType = UserType.PLAYER
    shorted_name: str


class ManagerResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)
    name: str