from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: Literal["dev", "prod"] = "dev"

    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=5000)
    WORKERS: int = Field(default=4)

    DATABASE_LOCAL: str = Field(default=...)
    DATABASE_REMOTE: str = Field(default="")
    DATABASE_REMOTE_DIRECT: str = Field(default="")
    API_KEY: str = Field(default="")

    ALLOWED_ORIGINS: list[str] = Field(default=["*"])

    # SECRET_KEY: str = Field(default="")

    @model_validator(mode='after')
    def check_prod_fields(self) -> "Settings":
        if self.ENV == "prod":
            missing = []
            if not self.DATABASE_REMOTE:
                missing.append("DATABASE_REMOTE")
            if not self.DATABASE_REMOTE_DIRECT:
                missing.append("DATABASE_REMOTE_DIRECT")
            if not self.API_KEY:
                missing.append("API_KEY")
            if missing:
                raise ValueError(f"Required in prod .env variables missing: {', '.join(missing)}")
        return self

    def get_database_url(self, direct: bool = False) -> str:
        if self.ENV == "dev":
            return self.DATABASE_LOCAL
        return self.DATABASE_REMOTE_DIRECT if direct else self.DATABASE_REMOTE

    @property
    def debug(self) -> bool:
        return self.ENV == "dev"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )


try:
    settings = Settings()
except Exception as e:
    raise RuntimeError(
        f"\n Configuration error: {e}"
        f"\n Missing environment variables."
        f"\n See .env.example for reference.\n"
    ) from None
