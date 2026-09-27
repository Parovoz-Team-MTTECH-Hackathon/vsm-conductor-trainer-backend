from .player import PlayerService
from .service import Service
from ..models import Player, Manager
from ..models.client import Management
from sqlalchemy import select
from fastapi import HTTPException, status

from ..schemas.client import PlayerResponse, ManagerResponse, PlayerGameStatisticResponse


class ManagerService(Service):
    async def get_management_players(self, manager_id: int) -> list[PlayerResponse]:
        result = await self.session.scalars(
            select(Player).join(
                Management, Management.player_id == Player.client_id
            ).where(Management.manager_id == manager_id)
        )
        players: list[Player] = list(result.all())
        return [PlayerResponse.model_validate(player) for player in players]

    async def profile(self, manager_id: int) -> ManagerResponse:
        result = await self.session.scalars(select(Manager).where(Manager.client_id == manager_id))
        manager: Manager | None = result.one_or_none()
        if manager is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return ManagerResponse.model_validate(manager)


    async def kick(self, manager_id: int, player_id: int):
        result = await self.session.scalars(
            select(Management).where(Management.manager_id == manager_id, Management.player_id == player_id)
        )
        management: Management | None = result.one_or_none()

        if management is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Management not found"
            )

        await self.session.delete(management)
        await self.session.commit()


    async def edit(self, manager_id: int, name: str) -> ManagerResponse:
        result = await self.session.scalars(select(Manager).where(Manager.client_id == manager_id))
        manager: Manager | None = result.one_or_none()
        if manager is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        if name.isspace():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Manager's name is empty"
            )
        if len((await self.session.scalars(select(Manager).where(Manager.name == name))).all()) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Manager with this name already exists"
            )
        manager.name = name
        await self.session.commit()
        await self.session.refresh(manager)
        return ManagerResponse.model_validate(manager)


    async def get_player_game_statistic(self, manager_id: int, player_id: int) -> PlayerGameStatisticResponse:
        if player_id not in self.get_management_players(manager_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )
        return await PlayerService(self.session).get_player_game_statistic(player_id=player_id)