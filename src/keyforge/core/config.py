from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    alembic_database_url: str
    redis_url: str
    secret_key: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
