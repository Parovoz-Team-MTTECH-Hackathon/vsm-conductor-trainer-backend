from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin, get_current_manager
from ..models import Manager
from ..schemas.client import ManagerResponse, PlayerResponse
from ..schemas.scenario import PlayerGameStatistic

router = APIRouter(
    prefix="/manager",
    tags=["Руководитель"],
)


@router.get("/profile")
async def profile(
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_admin)
) -> ManagerResponse:
    # todo
    ...


@router.get("/players")
async def manageable_players_list(
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> list[PlayerResponse]:
    # todo
    ...


@router.get("/kick")
async def kick_manageable_player(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
):
    # todo
    ...


@router.post("/profile/edit")
async def edit_profile(
        name: str,
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
):
    # todo
    ...


@router.get("/statistic")
async def manageable_player_statistic(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> PlayerGameStatistic:
    # todo
    ...