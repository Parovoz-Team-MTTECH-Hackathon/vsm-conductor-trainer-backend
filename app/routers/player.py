from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_player, get_current_user
from ..models import Player, User
from ..schemas.client import PlayerResponse, PublicPlayerResponse, PlayerShortGameStatisticResponse
from ..schemas.client import PlayerGameStatisticResponse
from ..services.player import PlayerService

router = APIRouter(
    prefix="/player",
    tags=["Игрок"],
)


@router.get("/profile")
async def profile(
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> PlayerResponse:
    return await PlayerService(session=session).profile(player_id=player.client_id)

@router.get("/public")
async def public_profile(
        player_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> PublicPlayerResponse:
    return await PlayerService(session=session).public(player_id=player_id)

@router.post("/profile/edit")
async def edit_profile(
        first_name: str | None,
        last_name: str | None,
        patronymic_name: str | None,
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> PlayerResponse:
    return await PlayerService(session=session).edit(first_name=first_name,
                                                     last_name=last_name,
                                                     patronymic_name=patronymic_name,
                                                     player_id=player.client_id)

@router.get("/join")
async def join(
        manager_id: int,
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> Response:
    await PlayerService(session=session).join(manager_id=manager_id, player_id=player.client_id)
    return Response()


@router.get("/statistic")
async def statistic(
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> PlayerGameStatisticResponse:
    return await PlayerService(session=session).get_player_game_statistic(player_id=player.client_id)


@router.get("/top")
async def top(
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> list[PlayerShortGameStatisticResponse]:
    return await PlayerService(session=session).get_top()