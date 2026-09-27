from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin, get_current_manager
from ..models import Manager
from ..schemas.client import ManagerResponse, PlayerResponse
from ..services.manager import ManagerService
from ..services.player import PlayerGameStatisticResponse

router = APIRouter(
    prefix="/manager",
    tags=["Руководитель"],
)


@router.get("/profile")
async def profile(
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> ManagerResponse:
    return await ManagerService(session).profile(manager.client_id)


@router.get("/players")
async def manageable_players_list(
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> list[PlayerResponse]:
    return await ManagerService(session).get_management_players(manager.client_id)


@router.get("/kick")
async def kick_manageable_player(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> Response:
    await ManagerService(session).kick(player_id=player_id, manager_id=manager.client_id)
    return Response()



@router.post("/profile/edit")
async def edit_profile(
        name: str,
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> ManagerResponse:
    return await ManagerService(session).edit(name=name, manager_id=manager.client_id)


@router.get("/statistic")
async def manageable_player_statistic(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        manager: Manager = Depends(get_current_manager)
) -> PlayerGameStatisticResponse:
    return await ManagerService(session).get_player_game_statistic(player_id=player_id, manager_id=manager.client_id)