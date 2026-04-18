import logging
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    APP_ENV: Literal["dev", "prod"] = "dev"
    DB_ENV: Literal["local", "remote"] = "local"

    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=5000)
    WORKERS: int = Field(default=4)

    DATABASE_LOCAL: str = Field(default=...)
    DATABASE_REMOTE: str = Field(default="")
    DATABASE_REMOTE_DIRECT: str = Field(default="")
    API_KEY: str = Field(default="")

    ALLOWED_ORIGINS: list[str] = Field(default=["*"])
    FORCE_HTTPS: bool = Field(default=True)

    # SECRET_KEY: str = Field(default="")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )

    @model_validator(mode='after')
    def check_prod_fields(self) -> "Settings":
        if self.APP_ENV != "prod":
            return self

        missing = [
            field
            for field, value in {
                "DATABASE_REMOTE": self.DATABASE_REMOTE,
                "DATABASE_REMOTE_DIRECT": self.DATABASE_REMOTE_DIRECT,
                "API_KEY": self.API_KEY,
            }.items()
            if not value
        ]

        if missing:
            raise ValueError(f"Missing required prod variables: {', '.join(missing)}")
        return self

    def get_database_url(self, direct: bool = False) -> str:
        if self.DB_ENV == "local":
            return self.DATABASE_LOCAL
        return self.DATABASE_REMOTE_DIRECT if direct else self.DATABASE_REMOTE

    @property
    def debug(self) -> bool:
        return self.APP_ENV == "dev"


def _load_settings() -> Settings:
    try:
        s = Settings()
        logger.debug(
            "Config loaded - env=%s db_target=%s debug=%s",
            s.APP_ENV, s.DB_ENV, s.debug
        )
        return s
    except Exception as e:
        logger.critical("Failed to load settings: %s", e)
        raise RuntimeError(
            f"\n Configuration error: {e}"
            f"\n See .env.example for reference.\n"
        ) from None


settings = _load_settings()
