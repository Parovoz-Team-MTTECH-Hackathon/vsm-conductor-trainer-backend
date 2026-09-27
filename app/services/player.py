from .service import Service
from ..models import Player, ClientType, UserType
from ..models.client import Management
from ..models.scenario import PlayerAchievement, ScenarioComplete, Scenario, Achievement
from sqlalchemy import select, func
from fastapi import HTTPException, status

from ..schemas.client import PlayerResponse, PublicPlayerResponse,PlayerShortGameStatisticResponse, PlayerGameStatisticResponse
from ..schemas.scenario import AchievementResponse, ScenarioResponse


class PlayerService(Service):
    async def profile(self, player_id: int) -> PlayerResponse:
        result = await self.session.scalars(select(Player).where(Player.client_id == player_id))
        player: Player | None = result.one_or_none()
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return PlayerResponse.model_validate(player)

    async def public(self, player_id: int) -> PublicPlayerResponse:
        result = await self.session.scalars(select(Player).where(Player.client_id == player_id))
        player: Player | None = result.one_or_none()
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        if len(player.last_name)>0:
            return PublicPlayerResponse(
                shorted_name=f"{player.first_name} {player.last_name[0]}.",
                client_id=player.client_id,
                is_active=player.is_active,
                client_type=ClientType.USER,
                user_type=UserType.PLAYER
            )
        else:
            return PublicPlayerResponse(shorted_name=f"{player.first_name}",
                client_id=player.client_id,
                is_active=player.is_active,
                client_type=ClientType.USER,
                user_type=UserType.PLAYER
            )


    async def join(self, manager_id: int, player_id: int):
        result = await self.session.scalars(select(Management).where(Management.manager_id == manager_id,
                                                                     Management.player_id == player_id))
        if result.one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already joined"
            )
        manager = Management(
            player_id=player_id,
            manager_id=manager_id
        )
        self.session.add(manager)
        await self.session.commit()
        await self.session.refresh(manager)


    async def edit(self, player_id: int, first_name: str | None, last_name: str | None, patronymic_name: str | None) -> PlayerResponse:
        result = await self.session.scalars(select(Player).where(Player.client_id == player_id))
        player: Player | None = result.one_or_none()
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        if first_name is not None and not first_name.isspace():
            player.first_name = first_name
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Player's first name is empty"
            )
        if last_name is not None and not last_name.isspace():
            player.last_name = last_name
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Player's last name is empty"
            )
        if patronymic_name is not None and not patronymic_name.isspace():
            player.patronymic_name = patronymic_name
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Player's patronymic name is empty"
            )

        await self.session.commit()
        await self.session.refresh(player)
        return PlayerResponse.model_validate(player)


    async def get_player_game_statistic(self, player_id: int) -> PlayerGameStatisticResponse:
        player_achievements_result = await self.session.scalars(
            select(Achievement).join(
                PlayerAchievement,
                (
                    PlayerAchievement.scenario_id == Achievement.scenario_id
                ) & (
                    PlayerAchievement.achievement_name == Achievement.achievement_name
                )
            ).where(PlayerAchievement.player_id == player_id)
        )
        player_achievements = list(player_achievements_result.all())

        scenario_completes_result = await self.session.scalars(
            select(ScenarioComplete).where(ScenarioComplete.player_id == player_id)
        )
        completed_scenarios = list(scenario_completes_result.all())


        return PlayerGameStatisticResponse(
            player_id = player_id,
            achievements = [AchievementResponse.model_validate(achievement) for achievement in player_achievements],
            completed_scenarios= [scenario_complete.scenario_id for scenario_complete in completed_scenarios],
            score = sum(achievement.score_delta for achievement in player_achievements)
        )


    async def get_top(self) -> list[PlayerShortGameStatisticResponse]:
        score = func.coalesce(
            func.sum(Achievement.score_delta),
            0,
        ).label("score")

        result = await self.session.execute(
            select(Player, score)
            .join(
                PlayerAchievement,
                PlayerAchievement.player_id == Player.client_id,
                isouter=True,
            )
            .join(
                Achievement,
                (Achievement.scenario_id == PlayerAchievement.scenario_id)
                & (
                        Achievement.achievement_name
                        == PlayerAchievement.achievement_name
                ),
                isouter=True,
            )
            .group_by(Player.client_id)
            .order_by(score.desc())
            .limit(10)
        )

        return [
            PlayerShortGameStatisticResponse(
                player_id=player.client_id,
                score=score,
            )
            for player, score in result.all()
        ]
