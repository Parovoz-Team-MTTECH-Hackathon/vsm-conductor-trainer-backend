from .service import Service
from ..models import Integration, Client, Admin, Manager, Player
from sqlalchemy import select

from ..schemas.client import AdminResponse, PlayerResponse, ManagerResponse, IntegrationResponse
from fastapi import HTTPException, status


class AdminService(Service):
    async def inactivate_client(self, self_id: int, client_id: int):
        if self_id == client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Self user can't be deleted"
            )
        result = await self.session.scalars(select(Client).where(Client.client_id == client_id))
        client: Client | None = result.one_or_none()
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        client.is_active = False
        await self.session.commit()
        await self.session.refresh(client)

    async def activate_client(self, client_id: int):
        result = await self.session.scalars(select(Client).where(Client.client_id == client_id))
        client: Client | None = result.one_or_none()
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        client.is_active = True
        await self.session.commit()
        await self.session.refresh(client)

    async def profile(self, admin_id: int) -> AdminResponse:
        result = await self.session.scalars(select(Admin).where(Admin.client_id == admin_id))
        admin: Admin | None = result.one_or_none()
        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        return AdminResponse.model_validate(admin)

    async def players(self) -> list[PlayerResponse]:
        result = await self.session.scalars(select(Player))
        players: list[Player] = list(result.all())
        return [PlayerResponse.model_validate(player) for player in players]

    async def managers(self) -> list[ManagerResponse]:
        result = await self.session.scalars(select(Manager))
        managers: list[Manager] = list(result.all())
        return [ManagerResponse.model_validate(manager) for manager in managers]

    async def integrations(self) -> list[IntegrationResponse]:
        result = await self.session.scalars(select(Integration))
        integrations: list[Integration] = list(result.all())
        return [IntegrationResponse.model_validate(integration) for integration in integrations]