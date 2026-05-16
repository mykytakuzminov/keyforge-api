from uuid import UUID

from fastapi import APIRouter, Depends

from keyforge.users.dependencies import get_user_service
from keyforge.users.models import User
from keyforge.users.schemas import UserCreate, UserResponse, UserUpdate
from keyforge.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UserResponse)
async def get_user_by_email(
    email: str, service: UserService = Depends(get_user_service)
) -> User:
    return await service.get_by_email(email)


@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate, service: UserService = Depends(get_user_service)
) -> User:
    return await service.create(user_in)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID, service: UserService = Depends(get_user_service)
) -> User:
    return await service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def change_user(
    user_id: UUID, user_in: UserUpdate, service: UserService = Depends(get_user_service)
) -> User:
    return await service.update(user_id, user_in)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID, service: UserService = Depends(get_user_service)
) -> None:
    await service.delete(user_id)
