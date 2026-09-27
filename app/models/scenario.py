from sqlalchemy import ForeignKey, DateTime, JSON, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from datetime import datetime



class Scenario(Base):
    __tablename__ = "scenarios"

    scenario_id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    icon: Mapped[str] = mapped_column(nullable=False)
    scenario_project_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    scenario_compiled_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    creation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ScenarioComplete(Base):
    __tablename__ = "scenario_completes"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.client_id", ondelete="CASCADE"), primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.scenario_id", ondelete="CASCADE"), primary_key=True)



class Achievement(Base):
    __tablename__ = "achievements"

    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.scenario_id", ondelete="CASCADE"), primary_key=True)
    achievement_name: Mapped[str] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    icon: Mapped[str] = mapped_column(nullable=False)
    score_delta: Mapped[int] = mapped_column(nullable=False)


class PlayerAchievement(Base):
    __tablename__ = "player_achievements"

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.client_id", ondelete="CASCADE"),
        primary_key=True,
    )

    scenario_id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    achievement_name: Mapped[str] = mapped_column(
        primary_key=True,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["scenario_id", "achievement_name"],
            ["achievements.scenario_id", "achievements.achievement_name"],
            ondelete="CASCADE",
        ),
    )
