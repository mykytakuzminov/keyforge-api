from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.auth.schemas import TokenPayload
from keyforge.auth.service import AuthService
from keyforge.core.database import get_db
from keyforge.core.redis import get_redis
from keyforge.core.security import verify_access_token
from keyforge.users.enums import UserRole

security = HTTPBearer()


def get_auth_service(
    db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)
) -> AuthService:
    return AuthService(db, redis)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenPayload:
    token = credentials.credentials
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload["sub"]
    role = payload["role"]
    return TokenPayload(user_id=user_id, role=role)


def get_current_admin(
    current_user: TokenPayload = Depends(get_current_user),
) -> TokenPayload:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


async def rate_limit(request: Request, redis: Redis = Depends(get_redis)) -> None:
    ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{ip}"

    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 60)

    if count > 5:
        raise HTTPException(status_code=429, detail="Too many requests")
