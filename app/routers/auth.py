from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..dependencies import get_current_admin
from ..models import Admin
from ..schemas.auth import UserLoginRequest, RefreshRequest, TokenResponse, PlayerSignupRequest, \
    IntegrationSignupRequest, ManagerSignupRequest, IntegrationLoginRequest, DeleteRequest
from ..services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
)


@router.post("/login/user", response_model=TokenResponse)
async def login_user(data: UserLoginRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    return await AuthService(session).login_user(email=str(data.email), password=data.password)


@router.post("/signup/player", response_model=TokenResponse)
async def signup_player(data: PlayerSignupRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    return await AuthService(session).signup_player(
        email=str(data.email),
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic_name=data.patronymic_name
    )

@router.post("/signup/manager", response_model=TokenResponse)
async def signup_manager(data: ManagerSignupRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    return await AuthService(session).signup_manager(
        email=str(data.email),
        password=data.password,
        name=data.name
    )

@router.post("/login/integration", response_model=TokenResponse)
async def login_integration(data: IntegrationLoginRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    return await AuthService(session).login_integration(key=data.key, secret=data.secret)


@router.post("/signup/integration", response_model=TokenResponse)
async def signup_integration(
        data: IntegrationSignupRequest,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> TokenResponse:
    return await AuthService(session).signup_integration(key=data.key, secret=data.secret, name=data.name)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    return await AuthService(session).refresh(data.refresh_token)


@router.post("/delete")
async def delete(
        data: DeleteRequest,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await AuthService(session).delete_client(self_id=admin.client_id, client_id=data.client_id)
    return Response()

