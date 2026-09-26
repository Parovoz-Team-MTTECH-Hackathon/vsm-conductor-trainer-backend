from ..models import Integration, Client
from ..models.client import User
from ..schemas.auth import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..security.hashing import verify_value
from ..security.tokens import create_access_token, create_refresh_token, decode_token
import jwt


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login_user(self, email: str, password: str) -> TokenResponse:
        result = await self.session.scalars(select(User).where(User.email == email))
        user: User | None = result.one_or_none()
        if user is None:
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("Client is inactive (maybe blocked)")
        if not verify_value(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return TokenResponse(access_token=create_access_token(user.client_id),
                             refresh_token=create_refresh_token(user.client_id))

    async def login_integration(self, key: str, secret: str) -> TokenResponse:
        result = await self.session.scalars(select(Integration).where(Integration.key == key))
        integration: Integration | None = result.one_or_none()
        if integration is None:
            raise ValueError("Invalid credentials")
        if not integration.is_active:
            raise ValueError("Client is inactive (maybe blocked)")
        if not verify_value(secret, integration.secret_hash):
            raise ValueError("Invalid credentials")
        return TokenResponse(access_token=create_access_token(integration.client_id),
                             refresh_token=create_refresh_token(integration.client_id))

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token")
        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        client_id = payload.get("sub")

        if client_id is None:
            raise ValueError("Invalid refresh token")

        try:
            int_client_id: int = int(client_id)
        except (TypeError, ValueError):
            raise ValueError("Invalid client id")
        result = await self.session.scalars(select(Client).where(Client.client_id == int_client_id))

        client: Client | None = result.one_or_none()

        if client is None:
            raise ValueError("Invalid refresh token")

        if not client.is_active:
            raise ValueError("Client is inactive (maybe blocked)")

        return TokenResponse(
            access_token=create_access_token(client.client_id),
            refresh_token=create_refresh_token(client.client_id),
        )