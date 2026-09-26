from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin, get_current_manager, get_current_player
from ..models import Manager, Player, Client
from ..schemas.client import ManagerResponse, PlayerResponse, PublicPlayerResponse
from ..schemas.scenario import PlayerGameStatistic

router = APIRouter(
    prefix="/player",
    tags=["Игрок"],
)


@router.get("/profile")
async def profile(
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> PlayerResponse:
    # todo
    ...

@router.get("/public")
async def public_profile(
        player_is: int,
        session: AsyncSession = Depends(get_session),
        client: Client = Depends(get_current_player)
) -> PublicPlayerResponse:
    # todo
    ...

@router.post("/profile/edit")
async def edit_profile(
        first_name: str | None,
        last_name: str | None,
        patronymic_name: str | None,
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> PublicPlayerResponse:
    # todo
    ...

@router.get("/join")
async def join(
        manager_id: int,
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> Response:
    # todo
    ...


@router.get("/statistic")
async def statistic(
        session: AsyncSession = Depends(get_session),
        player: Player = Depends(get_current_player)
) -> PlayerGameStatistic:
    # todo
    ...