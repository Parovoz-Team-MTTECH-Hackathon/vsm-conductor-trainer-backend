from pydantic import BaseModel, ConfigDict
from app.models import ClientType, UserType
from datetime import datetime


class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    scenario_id: int
    label: str
    description: str
    icon: str
    creation_time: datetime

class AchievementResponse(BaseModel):
    scenario_id: int
    achievement_name: str
    label: str
    description: str
    icon: str
    score_delta: int

class PlayerGameStatistic(BaseModel):
    player_id: int
    player_achievements: list[AchievementResponse]
    completed_scenarios: list[ScenarioResponse]
    score: int
