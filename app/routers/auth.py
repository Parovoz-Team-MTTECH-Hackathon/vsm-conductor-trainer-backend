from fastapi import APIRouter, Depends, Response, status, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..dependencies import get_current_admin
from ..models import Admin
from ..schemas.auth import UserLoginRequest, TokenResponse, PlayerSignupRequest, \
    IntegrationSignupRequest, ManagerSignupRequest, IntegrationLoginRequest, DeleteRequest
from ..services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
)


@router.post("/login/user", response_model=TokenResponse)
async def login_user(response: Response, data: UserLoginRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    token_response: TokenResponse = await AuthService(session).login_user(email=str(data.email), password=data.password)
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return token_response


@router.post("/signup/player", response_model=TokenResponse)
async def signup_player(response: Response, data: PlayerSignupRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    token_response: TokenResponse = await AuthService(session).signup_player(
        email=str(data.email),
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic_name=data.patronymic_name
    )
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return token_response

@router.post("/signup/manager", response_model=TokenResponse)
async def signup_manager(
        data: ManagerSignupRequest,
        response: Response, session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> TokenResponse:
    token_response: TokenResponse = await AuthService(session).signup_manager(
        email=str(data.email),
        password=data.password,
        name=data.name
    )

    return token_response


@router.post("/login/integration", response_model=TokenResponse)
async def login_integration(response: Response, data: IntegrationLoginRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    token_response: TokenResponse = await AuthService(session).login_integration(key=data.key, secret=data.secret)
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return token_response


@router.post("/signup/integration", response_model=TokenResponse)
async def signup_integration(
        response: Response,
        data: IntegrationSignupRequest,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> TokenResponse:
    token_response: TokenResponse = await AuthService(session).signup_integration(key=data.key, secret=data.secret, name=data.name)
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return token_response


@router.post("/refresh", response_model=TokenResponse)
async def refresh(response: Response, refresh_token : str | None = Cookie(default=None) , session: AsyncSession = Depends(get_session)) -> TokenResponse:
    token_response: TokenResponse = await AuthService(session).refresh(refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return token_response


@router.get("/logout", response_model=TokenResponse)
async def logout(response: Response) -> RedirectResponse:
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return RedirectResponse("/")


@router.post("/delete")
async def delete(
        data: DeleteRequest,
        session: AsyncSession = Depends(get_session),
        admin: Admin = Depends(get_current_admin)
) -> Response:
    await AuthService(session).delete_client(self_id=admin.client_id, client_id=data.client_id)
    return Response()


@router.post("/recovery")
async def recovery() -> Response:
    # Необходимо реализовать, если будут доступны сценарии восстановления пароля
    # (В рамках хакатона нет доступных сценариев, ибо для восстановления требуются
    # внешние сервисы с использованием SMTP-Email и т.п.)
    return Response(
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )