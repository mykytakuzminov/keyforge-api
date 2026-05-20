from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

from keyforge.auth.router import router as auth_router
from keyforge.clients.router import router as clients_router
from keyforge.core.config import settings
from keyforge.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.redis_client = Redis.from_url(settings.redis_url)
    yield
    await app.state.redis_client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(clients_router)
