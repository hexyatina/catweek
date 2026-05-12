import logging
from typing import Literal, List

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    APP_ENV: Literal["dev", "prod"] = "dev"
    DB_ENV: Literal["local", "remote"] = "local"

    HOST: str = "0.0.0.0"
    PORT: int = 5000
    WORKERS: int = 4

    DATABASE_URL_LOCAL: str = ""
    DATABASE_URL_REMOTE: str = ""
    DATABASE_URL_REMOTE_DIRECT: str = ""

    API_KEY: str = ""

    APP_VERSION: str = "0.0.0-dev"
    GIT_SHA: str = "unknown"

    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:8080",
            "http://localhost:5173",
        ]
    )
    CORS_API_PREFIX: str = Field(default="/api/*")

    FORCE_HTTPS: bool = True

    # SECRET_KEY: str = Field(default="")

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", extra="ignore"
    )

    @property
    def debug(self) -> bool:
        return self.APP_ENV == "dev"

    def get_database_url(self, direct: bool = False) -> str:
        if self.DB_ENV == "local":
            return self.DATABASE_URL_LOCAL
        return self.DATABASE_URL_REMOTE_DIRECT if direct else self.DATABASE_URL_REMOTE

    @model_validator(mode="after")
    def check_required_fields(self) -> "Settings":
        errors = []

        if self.DB_ENV == "remote":
            if not self.DATABASE_URL_REMOTE:
                errors.append("DB_ENV=remote requires DATABASE_URL_REMOTE to be set")

            if not self.DATABASE_URL_REMOTE_DIRECT:
                errors.append(
                    "DB_ENV=remote requires DATABASE_URL_REMOTE_DIRECT to be set"
                )

        # API_KEY only validated and used in prod mode.
        if self.APP_ENV == "prod":
            if not self.API_KEY:
                errors.append("APP_ENV=prod requires API_KEY to be set")

        if self.PORT <= 0 or self.PORT > 65535:
            errors.append("PORT must be in range 1-65535")

        if self.WORKERS <= 0:
            errors.append("WORKERS must be > 0")

        if errors:
            raise ValueError("\n".join(errors))

        return self


def load_settings() -> Settings:
    try:
        s = Settings()
        logger.debug(
            "Config loaded - env=%s db_target=%s debug=%s", s.APP_ENV, s.DB_ENV, s.debug
        )

        return s

    except Exception as e:
        logger.critical("Failed to load settings: %s", e)
        raise RuntimeError(
            f"\n Configuration error: {e}\n See .env.example for reference.\n"
        ) from None
