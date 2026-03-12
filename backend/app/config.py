from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    ENV: Literal["dev", "prod"] = "dev"

    DATABASE_LOCAL: str = Field(default=...)
    DATABASE_REMOTE: str = Field(default=...)
    SECRET_KEY: str = Field(default=...)

    @property
    def DATABASE_URL(self) -> str:
        return self.DATABASE_REMOTE if self.ENV == "prod" else self.DATABASE_LOCAL

    @property
    def DEBUG(self) -> bool:
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