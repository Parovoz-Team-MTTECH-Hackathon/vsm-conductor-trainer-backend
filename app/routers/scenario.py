from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin, get_current_manager, get_current_player, get_current_client, \
    get_current_user
from ..models import Manager, Player, Client, Admin, User
from ..schemas.client import ManagerResponse, PlayerResponse, PublicPlayerResponse
from ..schemas.scenario import ScenarioResponse

router = APIRouter(
    prefix="/scenario",
    tags=["Сценарий"],
)


@router.get("/list")
async def scenarios_list(
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> list[ScenarioResponse]:
    # todo
    ...

@router.get("/get")
async def scenario_get(
        scenario_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> JSONResponse:
    # todo
    ...

@router.get("/project")
async def scenario_project(
        scenario_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> JSONResponse:
    # todo
    ...


@router.post("/upload")
async def scenarios_upload(
        scenario_project_json: dict,
        scenario_compiled_json: dict,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    # todo
    ...


@router.get("/achieve")
async def achieve(
    scenario_id: int,
    achievement_name: str,
    session: AsyncSession = Depends(get_session),
    player: Player = Depends(get_current_player)
) -> Response:
    # todo
    ...

