import json

from .service import Service
from ..models.scenario import PlayerAchievement, ScenarioComplete, Scenario, Achievement
from sqlalchemy import select
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from ..schemas.scenario import AchievementResponse, ScenarioResponse


class ScenarioService(Service):
    async def create_scenario(self) -> ScenarioResponse:
        scenario = Scenario(
            label="New scenario",
            description="No description...",
            icon="",
            creation_time=datetime.now(),
            scenario_project_json="",
            scenario_compiled_json=dict(
                label="New scenario",
                description="No description...",
                icon=""
            )
        )
        self.session.add(scenario)
        await self.session.commit()
        return ScenarioResponse.model_validate(scenario)


    async def get_scenarios_list(self) -> list[ScenarioResponse]:
        result = await self.session.scalars(select(Scenario))
        return [ScenarioResponse.model_validate(scenario) for scenario in result.all()]


    async def delete_scenario(self, scenario_id: int):
        result = await self.session.scalars(
            select(Scenario).where(Scenario.scenario_id == scenario_id)
        )
        scenario: Scenario | None = result.one_or_none()

        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )

        await self.session.delete(scenario)
        await self.session.commit()


    async def get_scenario(self, scenario_id: int) -> JSONResponse:
        result = await self.session.scalars(select(Scenario).where(Scenario.scenario_id == scenario_id))
        scenario: Scenario | None = result.one_or_none()
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        return JSONResponse(content=scenario.scenario_compiled_json)


    async def get_project(self, scenario_id: int) -> JSONResponse:
        result = await self.session.scalars(select(Scenario).where(Scenario.scenario_id == scenario_id))
        scenario: Scenario | None = result.one_or_none()
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        return JSONResponse(content=scenario.scenario_project_json)


    async def upload(
            self,
            scenario_id: int,
            scenario_project_json: dict,
            scenario_compiled_json: dict
    ) -> ScenarioResponse:
        result = await self.session.scalars(select(Scenario).where(Scenario.scenario_id == scenario_id))
        scenario: Scenario | None = result.one_or_none()
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        scenario.scenario_project_json = scenario_project_json
        scenario.scenario_compiled_json = scenario_compiled_json

        nodes: dict | None = scenario_compiled_json.get("nodes")
        if nodes is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Scenario's nodes not found"
            )

        result = await self.session.scalars(
            select(Achievement).where(Achievement.scenario_id == scenario_id)
        )
        for achievement in result.all():
            await self.session.delete(achievement)


        try:
            scenario.name = scenario_compiled_json["nodes"]
            scenario.label = scenario_compiled_json["label"]
            scenario.description = scenario_compiled_json["description"]
            scenario.icon = scenario_compiled_json["icon"]
            scenario.creation_time = datetime.strptime(scenario_compiled_json["creation_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            for node in nodes:
                if nodes[node]["content_type"] == "achievement":
                    content = nodes[node]["content"]
                    image = nodes[content["icon"]]["content"]["resource"]
                    achievement = Achievement(
                        scenario_id=scenario_id,
                        achievement_name=content["name"],
                        label=content["label"],
                        description=content["description"],
                        icon=image,
                        score_delta=content["score_delta"]
                    )
                    self.session.add(achievement)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Scenario's achievement node fields are conflicting"
            )

        await self.session.commit()
        await self.session.refresh(scenario)
        return ScenarioResponse.model_validate(scenario)


    async def achieve(
            self,
            scenario_id: int,
            achievement_name: str,
            player_id: int
    ) -> AchievementResponse:
        result = await self.session.scalars(select(Scenario).where(
            Scenario.scenario_id == scenario_id,
        ))
        scenario: Scenario | None = result.one_or_none()
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )

        result = await self.session.scalars(select(Achievement).where(
            Achievement.scenario_id == scenario_id,
            Achievement.achievement_name == achievement_name
        ))
        achievement: Achievement | None = result.one_or_none()
        if achievement is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Achievement not found"
            )

        result = await self.session.scalars(select(PlayerAchievement).where(
            PlayerAchievement.scenario_id == scenario_id,
            PlayerAchievement.achievement_name == achievement_name,
            PlayerAchievement.player_id == player_id
        ))
        if result.one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already achieved"
            )
        playerAchievement = PlayerAchievement(
            scenario_id=scenario_id,
            achievement_name=achievement_name,
            player_id=player_id
        )
        self.session.add(playerAchievement)
        await self.session.commit()
        await self.session.refresh(playerAchievement)
        return AchievementResponse.model_validate(achievement)


    async def complete(
            self,
            scenario_id: int,
            player_id: int
    ) -> ScenarioResponse:
        result = await self.session.scalars(select(Scenario).where(
            Scenario.scenario_id == scenario_id,
        ))
        scenario: Scenario | None = result.one_or_none()
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )

        result = await self.session.scalars(select(ScenarioComplete).where(
            ScenarioComplete.scenario_id == scenario_id,
            ScenarioComplete.player_id == player_id
        ))
        if result.one_or_none() is None:
            scenario_complete = ScenarioComplete(
                scenario_id=scenario_id,
                player_id=player_id
            )
            self.session.add(scenario_complete)
            await self.session.commit()
            await self.session.refresh(scenario_complete)

        return ScenarioResponse.model_validate(scenario)