from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_LOCAL: str = "postgresql://user:pass@localhost:5432/local_db"
    DATABASE_REMOTE: str = "postgresql://prod_user:prod_pass@remote-host:5432/prod_db"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env"
    )

settings = Settings()