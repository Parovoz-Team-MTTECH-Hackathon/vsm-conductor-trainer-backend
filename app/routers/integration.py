from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_integration
from ..models import Manager, Integration
from ..schemas.client import ManagerResponse, PlayerResponse
from ..schemas.scenario import PlayerGameStatistic

router = APIRouter(
    prefix="/integration",
    tags=["Интеграция (Внешнее приложение)"],
)


@router.get("/manager/players")
async def manager_players_list(
        manager_id: int,
        session: AsyncSession = Depends(get_session),
        integration: Integration = Depends(get_current_integration)
) -> list[PlayerResponse]:
    # todo
    ...

@router.get("/player/statistic")
async def player_statistic(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        integration: Integration = Depends(get_current_integration)
) -> PlayerGameStatistic:
    # todo
    ...