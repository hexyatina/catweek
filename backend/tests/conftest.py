from pathlib import Path
from typing import Literal

import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config as AlembicConfig
from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from sqlalchemy.orm import Session

from app import create_app
from app.config import Settings
from app.extensions import db as _db
from app.models import Day

load_dotenv(".env.test", override=True)

ROOT = Path(__file__).parent.parent


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=None,
        extra="ignore"
    )
    DB_ENV: Literal["local", "remote", "test"] = "test"
    FORCE_HTTPS: bool = False
    ALLOWED_ORIGINS: list[str] = []


@pytest.fixture(scope="session")
def app():
    import os
    print(f"DEBUG: ENV URL IS {os.environ.get('DATABASE_URL_LOCAL')}")
    cfg = TestSettings()
    return create_app(settings=cfg)


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        alembic_config = AlembicConfig(str(ROOT / "alembic.ini"))
        alembic_config.set_main_option(
            "sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"]
        )
        alembic_config.set_main_option("script_location", str(ROOT / "migrations"))
        upgrade(alembic_config, "head")
        yield _db
        downgrade(alembic_config, "base")


@pytest.fixture(scope="function")
def db_session(db, app):
    with app.app_context():
        with _db.engine.connect() as connection:
            with connection.begin():
                session = Session(
                    bind=connection, join_transaction_mode="create_savepoint"
                )
                yield session
                session.close()


@pytest.fixture()
def client(app, db_session):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def day(db_session):
    obj = Day(id=1, name_uk="Понеділок", name_en="Monday")
    db_session.add(obj)
    db_session.flush()
    return obj
