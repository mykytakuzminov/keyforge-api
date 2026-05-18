import os

import pytest
from alembic.config import Config
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from alembic import command
from keyforge.auth.service import AuthService
from keyforge.users.service import UserService

if "DOCKER_HOST" not in os.environ:
    os.environ["DOCKER_HOST"] = (
        f"unix://{os.path.expanduser('~')}/.colima/default/docker.sock"
    )

os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"


@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:18-alpine") as postgres:
        sync_url = postgres.get_connection_url()
        async_url = sync_url.replace("postgresql+psycopg2", "postgresql+asyncpg")
        yield sync_url, async_url


@pytest.fixture(scope="session")
def redis_url():
    with RedisContainer("redis:8-alpine") as redis:
        host = redis.get_container_host_ip()
        port = redis.get_exposed_port(6379)
        yield f"redis://{host}:{port}"


@pytest.fixture(scope="session", autouse=True)
def run_migration(postgres_url):
    sync_url, _ = postgres_url
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture
def engine(postgres_url):
    _, async_url = postgres_url
    return create_async_engine(async_url)


@pytest.fixture
async def db_session(engine):
    AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession)
    async with AsyncSessionFactory() as session:
        yield session


@pytest.fixture
async def redis_client(redis_url):
    client = Redis.from_url(redis_url)
    yield client
    await client.aclose()


@pytest.fixture(autouse=True)
async def clean_db(db_session):
    yield
    await db_session.execute(
        text("TRUNCATE TABLE users, clients, refresh_tokens CASCADE")
    )
    await db_session.commit()


@pytest.fixture(autouse=True)
async def clean_redis(redis_client):
    yield
    await redis_client.flushall()


@pytest.fixture
def user_service(db_session):
    return UserService(db_session)


@pytest.fixture
def auth_service(db_session, redis_client):
    return AuthService(db_session, redis_client)
