from pydantic import BaseModel, ConfigDict
from app.models import ClientType, UserType
from app.schemas.scenario import AchievementResponse


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
    user_type: UserType = UserType.PLAYER
    shorted_name: str


class ManagerResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)
    name: str


class PlayerShortGameStatisticResponse(BaseModel):
    shorted_name: str
    player_id: int
    score: int

class PlayerGameStatisticResponse(PlayerShortGameStatisticResponse):
    achievements: list[AchievementResponse]
    completed_scenarios: list[int]