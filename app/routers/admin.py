from fastapi import APIRouter, Depends, Response
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
   return await AdminService(session).profile(admin.client_id)


@router.get("/inactivate")
async def inactivate_client(
        client_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await AdminService(session).inactivate_client(self_id=admin.client_id, client_id=client_id)
    return Response()


@router.get("/activate")
async def activate_client(
        client_id: int,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await AdminService(session).activate_client(client_id=client_id)
    return Response()


@router.get("/players")
async def players_list(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> list[PlayerResponse]:
    return await AdminService(session).players()


@router.get("/managers")
async def managers_list(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> list[ManagerResponse]:
    return await AdminService(session).managers()


@router.get("/integrations")
async def integrations_list(
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> list[IntegrationResponse]:
    return await AdminService(session).integrations()