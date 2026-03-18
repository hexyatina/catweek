from typing import Literal
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    ENV: Literal["dev", "prod"] = "dev"

    DATABASE_LOCAL: str = Field(default=...)
    DATABASE_REMOTE: str = Field(default="")
    DATABASE_REMOTE_DIRECT: str = Field(default="")
    API_KEY: str = Field(default="")

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

    @property
    def DATABASE_URL(self) -> str:
        return self.DATABASE_REMOTE if self.ENV == "prod" else self.DATABASE_LOCAL

    @property
    def DATABASE_URL_DIRECT(self) -> str:
        return self.DATABASE_REMOTE_DIRECT  if self.ENV == "prod" else self.DATABASE_LOCAL

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