from uuid import UUID

import pytest
from fastapi import HTTPException

from keyforge.core.security import (
    generate_secure_token,
    verify_access_token,
    verify_hashed_value,
)
from keyforge.tokens.repository import TokenRepository
from tests.constants import EMAIL, INVALID_PASSWORD, PASSWORD, TOKEN, USER_ID


async def test_authenticate(user_service, auth_service):
    user = await user_service.create(EMAIL, PASSWORD)
    authenticated_user = await auth_service.authenticate(EMAIL, PASSWORD)
    assert user.id == authenticated_user.id
    assert user.email == authenticated_user.email
    assert user.is_active == authenticated_user.is_active
    assert verify_hashed_value(PASSWORD, authenticated_user.hashed_password)


async def test_authenticate_not_found(auth_service):
    with pytest.raises(HTTPException, match="Invalid credentials"):
        await auth_service.authenticate(EMAIL, PASSWORD)


async def test_authenticate_invalid_password(user_service, auth_service):
    await user_service.create(EMAIL, PASSWORD)
    with pytest.raises(HTTPException, match="Invalid credentials"):
        await auth_service.authenticate(EMAIL, INVALID_PASSWORD)


async def test_save(auth_service, redis_client):
    await auth_service.save(TOKEN, UUID(USER_ID))
    token_repository = TokenRepository(redis_client)
    result = await token_repository.get(TOKEN)
    assert result == UUID(USER_ID)


async def test_refresh(user_service, auth_service):
    await user_service.create(EMAIL, PASSWORD)
    user = await auth_service.authenticate(EMAIL, PASSWORD)
    refresh_token = generate_secure_token()
    await auth_service.save(refresh_token, user.id)
    access_token = await auth_service.refresh(refresh_token)
    payload = verify_access_token(access_token)

    assert payload["sub"] == str(user.id)
    assert payload["role"] == user.role.value


async def test_refresh_invalid_token(auth_service):
    with pytest.raises(HTTPException, match="Invalid or expired token"):
        await auth_service.refresh(TOKEN)


async def test_refresh_user_not_found(user_service, auth_service):
    await user_service.create(EMAIL, PASSWORD)
    user = await auth_service.authenticate(EMAIL, PASSWORD)
    refresh_token = generate_secure_token()
    await auth_service.save(refresh_token, user.id)
    await user_service.delete(user.id)
    with pytest.raises(HTTPException, match="User not found"):
        await auth_service.refresh(refresh_token)


async def test_logout(user_service, auth_service):
    await user_service.create(EMAIL, PASSWORD)
    user = await auth_service.authenticate(EMAIL, PASSWORD)
    refresh_token = generate_secure_token()
    await auth_service.save(refresh_token, user.id)
    await auth_service.logout(refresh_token)
    with pytest.raises(HTTPException, match="Invalid or expired token"):
        await auth_service.refresh(TOKEN)
