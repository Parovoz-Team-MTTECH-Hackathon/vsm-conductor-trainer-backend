from pydantic import BaseModel, ConfigDict
from ..models.client import ClientType, UserType


class ClientRequest(BaseModel):
    client_id: int


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    client_id: int
    is_active: bool
    client_type: ClientType


class IntegrationRequest(BaseModel):
    key: str
    secret: str


class IntegrationResponse(ClientResponse):
    model_config = ConfigDict(from_attributes=True)
    name: str


class UserRequest(BaseModel):
    email: str
    password: str

class UserResponse(ClientResponse):
    model_config = ConfigDict(from_attributes=True)
    user_type: UserType

class AdminRequest(UserRequest): pass

class AdminResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)

class PlayerRequest(UserRequest):
    first_name: str
    last_name: str
    patronymic_name: str

class PlayerResponse(UserResponse):
    first_name: str
    last_name: str
    patronymic_name: str


class ManagerRequest(UserRequest):
    name: str

class ManagerResponse(UserResponse):
    name: str
