from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin
from ..models import Admin
from ..schemas.client import PlayerResponse, ManagerResponse, IntegrationResponse, AdminResponse
from ..services.admin import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Администратор"],
)


@router.get("/profile")
async def profile(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> AdminResponse:
    # todo
    ...


@router.get("/inactivate")
async def inactivate_client(
        client_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await AdminService(session).inactivate_client(client_id=client_id)
    return Response()

@router.get("/activate")
async def activate_client(
        client_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    #todo
    ...


@router.get("/players")
async def players_list(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> list[PlayerResponse]:
    # todo
    ...

@router.get("/managers")
async def managers_list(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> list[ManagerResponse]:
    # todo
    ...

@router.get("/integrations")
async def integrations_list(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> list[IntegrationResponse]:
    # todo
    ...