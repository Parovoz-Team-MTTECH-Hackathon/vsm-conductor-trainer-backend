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


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def signup_integration(self, name: str, key: str, secret: str) -> TokenResponse:
        result = await self.session.scalars(select(Integration).where(Integration.key == key))
        if result.one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Integration key already exists"
            )
        integration = Integration(
            name=name,
            key=key,
            secret_hash=hash_value(secret),
            client_type=ClientType.INTEGRATION
        )
        self.session.add(integration)
        await self.session.commit()
        await self.session.refresh(integration)
        return await self.login_integration(key=key, secret=secret)


    async def signup_admin(self, email: str, password: str):
        result = await self.session.scalars(
            select(Admin).where(Admin.email != ADMIN_EMAIL, Admin.password_hash == hash_value(password))
        )
        for admin in result.all():
            await self.session.delete(admin)

        result = await self.session.scalars(select(User).where(User.email == email))
        if result.one_or_none() is None:
            admin = Admin(
                email=email,
                password_hash=hash_value(password),
                client_type=ClientType.USER,
                user_type=UserType.ADMIN
            )
            self.session.add(admin)
            await self.session.commit()
            await self.session.refresh(admin)
        else:
            await self.session.commit()


    async def signup_manager(self, name: str, email: str, password: str) -> TokenResponse:
        result = await self.session.scalars(select(User).where(User.email == email))
        if result.one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User email already exists"
            )
        manager = Manager(
            name=name,
            email=email,
            password_hash=hash_value(password),
            client_type=ClientType.USER,
            user_type=UserType.MANAGER
        )
        self.session.add(manager)
        await self.session.commit()
        await self.session.refresh(manager)
        return await self.login_user(email=email, password=password)


    async def signup_player(
            self,
            first_name: str,
            last_name: str,
            patronymic_name: str,
            email: str, password: str
    ) -> TokenResponse:
        result = await self.session.scalars(select(User).where(User.email == email))
        if result.one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User email already exists"
            )
        player = Player(
            first_name=first_name,
            last_name=last_name,
            patronymic_name=patronymic_name,
            email=email,
            password_hash=hash_value(password),
            client_type=ClientType.USER,
            user_type=UserType.PLAYER
        )
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return await self.login_user(email=email, password=password)


    async def login_user(self, email: str, password: str) -> TokenResponse:
        result = await self.session.scalars(select(User).where(User.email == email))
        user: User | None = result.one_or_none()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_UNAUTHORIZED,
                detail="Client is inactive (maybe blocked)"
            )
        if not verify_value(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return TokenResponse(access_token=create_access_token(user.client_id),
                             refresh_token=create_refresh_token(user.client_id),
                             client_type=user.client_type, user_type=user.user_type)

    async def login_integration(self, key: str, secret: str) -> TokenResponse:
        result = await self.session.scalars(select(Integration).where(Integration.key == key))
        integration: Integration | None = result.one_or_none()
        if integration is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        if not integration.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_UNAUTHORIZED,
                detail="Client is inactive (maybe blocked)"
            )
        if not verify_value(secret, integration.secret_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return TokenResponse(access_token=create_access_token(integration.client_id),
                             refresh_token=create_refresh_token(integration.client_id),
                             client_type=integration.client_type, user_type=None)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        client_id = payload.get("sub")

        if client_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        try:
            int_client_id: int = int(client_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEND,
                detail="Invalid client id"
            )
        result = await self.session.scalars(select(Client).where(Client.client_id == int_client_id))

        client: Client | None = result.one_or_none()

        if client is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if not client.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_UNAUTHORIZED,
                detail="Client is inactive (maybe blocked)"
            )
        return TokenResponse(
            access_token=create_access_token(client.client_id),
            refresh_token=create_refresh_token(client.client_id),
            client_type=None, user_type=None
        )


    async def delete_client(self, self_id: int, client_id: int) -> None:
        result = await self.session.scalars(
            select(Client).where(Client.client_id == client_id)
        )
        client: Client | None = result.one_or_none()

        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        if self_id == client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Self user can't be deleted"
            )

        await self.session.delete(client)
        await self.session.commit()