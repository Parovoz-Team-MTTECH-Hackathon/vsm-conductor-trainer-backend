from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User, Admin, Player, Manager, Integration, Client
from app.security.tokens import decode_token
import jwt
from app.database import get_session


security = HTTPBearer()


async def get_current_client_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

    int_client_id = payload.get("sub")

    if int_client_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has no data"
        )

    try:
        return int(int_client_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token data"
        )


async def get_current_client(
        client_id: int = Depends(get_current_client_id),
        session: AsyncSession = Depends(get_session)
) -> Client:
    result = await session.scalars(select(Client).where(Client.client_id == client_id))
    client: Client | None = result.one_or_none()
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown access token or access denied"
        )
    if not client.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client is inactive (maybe blocked)"
        )
    return client


async def get_current_integration(
        client_id: int = Depends(get_current_client_id),
        session: AsyncSession = Depends(get_session)
) -> Integration:
    result = await session.scalars(select(Integration).where(Integration.client_id == client_id))
    integration: Integration | None = result.one_or_none()
    if integration is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown access token or access denied"
        )
    if not integration.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client is inactive (maybe blocked)"
        )
    return integration


async def get_current_user(
        client_id: int = Depends(get_current_client_id),
        session: AsyncSession = Depends(get_session)
) -> User:
    result = await session.scalars(select(User).where(User.client_id == client_id))
    user: User | None = result.one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown access token or access denied"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client is inactive (maybe blocked)"
        )
    return user


async def get_current_admin(
        client_id: int = Depends(get_current_client_id),
        session: AsyncSession = Depends(get_session)
) -> Admin:
    result = await session.scalars(select(Admin).where(Admin.client_id == client_id))
    admin: Admin | None = result.one_or_none()
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown access token or access denied"
        )
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client is inactive (maybe blocked)"
        )
    return admin


async def get_current_player(
        client_id: int = Depends(get_current_client_id),
        session: AsyncSession = Depends(get_session)
) -> Player:
    result = await session.scalars(select(Player).where(Player.client_id == client_id))
    player: Player | None = result.one_or_none()
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown access token or access denied"
        )
    if not player.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client is inactive (maybe blocked)"
        )
    return player


async def get_current_manager(
        client_id: int = Depends(get_current_client_id),
        session: AsyncSession = Depends(get_session)
) -> Manager:
    result = await session.scalars(select(Manager).where(Manager.client_id == client_id))
    manager: Manager | None = result.one_or_none()
    if manager is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unknown access token or access denied"
        )
    if not manager.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client is inactive (maybe blocked)"
        )
    return manager