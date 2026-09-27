from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_integration
from ..models import Integration
from ..schemas.client import PlayerResponse
from ..services.manager import ManagerService
from ..services.player import PlayerService, PlayerGameStatisticResponse

router = APIRouter(
    prefix="/integration",
    tags=["Интеграция (Внешнее приложение)"],
)


@router.get("/manager-players")
async def manager_players_list(
        manager_id: int,
        session: AsyncSession = Depends(get_session),
        integration: Integration = Depends(get_current_integration)
) -> list[PlayerResponse]:
    return await ManagerService(session).get_management_players(manager_id)


@router.get("/player-statistic")
async def player_statistic(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        integration: Integration = Depends(get_current_integration)
) -> PlayerGameStatisticResponse:
    return await PlayerService(session).get_player_game_statistic(player_id)