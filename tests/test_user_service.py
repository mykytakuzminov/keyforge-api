import pytest
from fastapi import HTTPException

from keyforge.users.enums import UserRole
from tests.constants import EMAIL, NEW_EMAIL, NEW_PASSWORD, PASSWORD, USER_ID


async def test_create_user(user_service):
    user = await user_service.create(EMAIL, PASSWORD)
    assert user.id is not None
    assert user.email == EMAIL
    assert user.hashed_password != PASSWORD
    assert user.role == UserRole.member


async def test_get_by_id(user_service):
    created_user = await user_service.create(EMAIL, PASSWORD)
    fetched_user = await user_service.get_by_id(created_user.id)
    assert created_user.id == fetched_user.id
    assert created_user.email == fetched_user.email
    assert created_user.hashed_password == fetched_user.hashed_password
    assert created_user.role == fetched_user.role


async def test_get_by_id_user_not_found(user_service):
    with pytest.raises(HTTPException, match="User not found"):
        await user_service.get_by_id(USER_ID)


async def test_get_by_email(user_service):
    created_user = await user_service.create(EMAIL, PASSWORD)
    fetched_user = await user_service.get_by_email(created_user.email)
    assert created_user.id == fetched_user.id
    assert created_user.email == fetched_user.email
    assert created_user.hashed_password == fetched_user.hashed_password
    assert created_user.role == fetched_user.role


async def test_get_by_email_user_not_found(user_service):
    with pytest.raises(HTTPException, match="User not found"):
        await user_service.get_by_email(EMAIL)


async def test_update_email(user_service):
    created_user = await user_service.create(EMAIL, PASSWORD)
    original_email = created_user.email
    updated_user = await user_service.update(created_user.id, NEW_EMAIL, None)
    assert updated_user.email != original_email
    assert updated_user.email == NEW_EMAIL


async def test_update_password(user_service):
    created_user = await user_service.create(EMAIL, PASSWORD)
    original_hash = created_user.hashed_password
    updated_user = await user_service.update(created_user.id, None, NEW_PASSWORD)
    assert updated_user.hashed_password != original_hash
    assert updated_user.hashed_password != NEW_PASSWORD
    assert updated_user.hashed_password is not None


async def test_update_user_not_found(user_service):
    with pytest.raises(HTTPException, match="User not found"):
        await user_service.update(USER_ID, EMAIL, None)


async def test_delete(user_service):
    user = await user_service.create(EMAIL, PASSWORD)
    await user_service.delete(user.id)
    with pytest.raises(HTTPException, match="User not found"):
        await user_service.get_by_id(user.id)
