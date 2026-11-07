from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/connect"
    redis_url: str = "redis://localhost:6379/0"
    log_level: str = "INFO"

    admin_ids: list[int] = []
    max_active_memberships: int | None = 10  # None = без лимита (BR-1, D-10)
    use_webhook: bool = False  # dev — polling, prod — webhook (R11)

    @field_validator("admin_ids", mode="before")
    @classmethod
    def split_admin_ids(cls, value: object) -> object:
        """ADMIN_IDS=123,456 из .env превращается в list[int]."""
        if isinstance(value, str):
            return [int(x) for x in value.split(",") if x.strip()]
        return value


settings = Settings()
