from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "FastAPI Celery Flower Sample"
    redis_url: str = "redis://redis:6379/0"
    database_url: str = "postgresql+psycopg2://app:app@postgres:5432/app"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
