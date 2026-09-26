from ..config import ADMIN_EMAIL
from ..models import Integration, Client, Admin, Manager, Player
from ..models.client import User, ClientType, UserType
from ..schemas.auth import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..security.hashing import verify_value, hash_value
from ..security.tokens import create_access_token, create_refresh_token, decode_token
import jwt
from fastapi import HTTPException, status


class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def inactivate_client(self, client_id):
        result = await self.session.scalars(select(Client).where(Client.client_id == client_id))
        client: Client | None = result.one_or_none()
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        client.is_active = False
        await self.session.commit()
        await self.session.refresh(client)