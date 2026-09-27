from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin, get_current_player, get_current_user
from ..models import Player, Admin, User
from ..schemas.scenario import ScenarioResponse, AchievementResponse
from ..services.scenario import ScenarioService

router = APIRouter(
    prefix="/scenario",
    tags=["Сценарий"],
)


@router.get("/list")
async def scenarios_list(
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> list[ScenarioResponse]:
    return await ScenarioService(session).get_scenarios_list()


@router.get("/create")
async def create_scenario(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> ScenarioResponse:
    return await ScenarioService(session).create_scenario()


@router.get("/delete")
async def delete_scenario(
        scenario_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await ScenarioService(session).delete_scenario(scenario_id)
    return Response()


@router.get("/get")
async def get_scenario(
        scenario_id: int,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> JSONResponse:
    return await ScenarioService(session).get_scenario(scenario_id)


@router.get("/project")
async def project_scenario(
        scenario_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> JSONResponse:
    return await ScenarioService(session).get_project(scenario_id)


@router.post("/upload")
async def upload_scenario(
        scenario_id: int,
        scenario_project_json: dict,
        scenario_compiled_json: dict,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await ScenarioService(session).upload(scenario_id, scenario_project_json, scenario_compiled_json)
    return Response()


@router.get("/achieve")
async def achieve(
    scenario_id: int,
    achievement_name: str,
    session: AsyncSession = Depends(get_session),
    player: Player = Depends(get_current_player)
) -> AchievementResponse:
    return await ScenarioService(session).achieve(scenario_id=scenario_id,
                                                  achievement_name=achievement_name,
                                                  player_id=player.client_id)


@router.get("/complete")
async def complete(
    scenario_id: int,
    session: AsyncSession = Depends(get_session),
    player: Player = Depends(get_current_player)
) -> ScenarioResponse:
    return await ScenarioService(session).complete(scenario_id=scenario_id, player_id=player.client_id)
