import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from keyforge.core.config import settings
from keyforge.users.enums import UserRole

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
pwd_context = CryptContext(schemes=["bcrypt"])


def create_access_token(user_id: UUID, role: UserRole) -> str:
    payload = {
        "sub": str(user_id),
        "role": role.value,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return str(jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM))


def verify_access_token(token: str) -> dict[str, object] | None:
    try:
        payload: dict[str, object] = jwt.decode(
            token, settings.secret_key, algorithms=ALGORITHM
        )
        return payload
    except JWTError:
        return None


def hash_value(value: str) -> str:
    return str(pwd_context.hash(value))


def verify_hashed_value(plain: str, hashed: str) -> bool:
    return bool(pwd_context.verify(plain, hashed))


def generate_secure_token() -> str:
    return secrets.token_urlsafe(32)
