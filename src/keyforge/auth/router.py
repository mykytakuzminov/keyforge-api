from fastapi import APIRouter, Depends

from keyforge.auth.dependencies import get_auth_service, get_current_user
from keyforge.auth.schemas import (
    LoginRequest,
    TokenPayload,
    TokenRequest,
    TokenResponse,
)
from keyforge.auth.service import AuthService
from keyforge.core.security import (
    create_access_token,
    generate_secure_token,
)
from keyforge.users.dependencies import get_user_service
from keyforge.users.models import User
from keyforge.users.schemas import UserCreate, UserResponse
from keyforge.users.service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate, service: UserService = Depends(get_user_service)
) -> User:
    return await service.create(user_in.email, user_in.password)


@router.post("/token", response_model=TokenResponse)
async def login(
    user_in: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    user = await auth_service.authenticate(user_in.email, user_in.password)
    access_token = create_access_token(user.id, user.role)
    refresh_token = generate_secure_token()
    await auth_service.save(refresh_token, user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: TokenRequest, auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    access_token = await auth_service.refresh(request.token)
    return TokenResponse(access_token=access_token, refresh_token=request.token)


@router.post("/logout", status_code=204)
async def logout(
    request: TokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
    _: TokenPayload = Depends(get_current_user),
) -> None:
    await auth_service.logout(request.token)


@router.get("/userinfo", response_model=UserResponse)
async def userinfo(
    user_service: UserService = Depends(get_user_service),
    current_user: TokenPayload = Depends(get_current_user),
) -> User:
    return await user_service.get_by_id(current_user.user_id)
