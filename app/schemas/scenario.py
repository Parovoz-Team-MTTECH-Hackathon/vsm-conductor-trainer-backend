from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    scenario_id: int
    label: str
    description: str
    icon: str
    creation_time: datetime


class AchievementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    scenario_id: int
    achievement_name: str
    label: str
    description: str
    icon: str
    score_delta: int
