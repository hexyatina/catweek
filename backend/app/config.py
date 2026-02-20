from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    ENV: Literal["dev", "prod"] = "dev"

    DATABASE_LOCAL: str = "postgresql://user:pass@localhost:5432/local_db"
    DATABASE_REMOTE: str = "postgresql://prod_user:prod_pass@remote-host:5432/prod_db"

    @property
    def DATABASE_URL(self) -> str:
        return self.DATABASE_REMOTE if self.ENV == "prod" else self.DATABASE_LOCAL

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
