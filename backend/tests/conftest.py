import os
from pathlib import Path

import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config as AlembicConfig

from app import create_app
from app.config import Settings
from app.extensions import db as _db
from app.models import Day

ROOT = Path(__file__).parent.parent


class TestSettings(Settings):
    model_config = Settings.model_config

    APP_ENV: str = "dev"
    DB_ENV: str = "local"
    DATABASE_LOCAL: str = os.environ.get(
        "TEST_DATABASE_LOCAL",
        "postgresql+psycopg://postgres:1845@localhost:5432/test_catweek"
    )
    FORCE_HTTPS: bool = False
    ALLOWED_ORIGINS: list[str] = []


@pytest.fixture(scope="session")
def app():
    cfg = TestSettings()
    application = create_app(settings=cfg)
    return application


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        alembic_config = AlembicConfig(str(ROOT / "alembic.ini"))
        alembic_config.set_main_option("sqlalchemy.url",
                                       app.config["SQLALCHEMY_DATABASE_URI"]
                                       )
        alembic_config.set_main_option("script_location", str(ROOT / "migrations"))
        upgrade(alembic_config, "head")
        yield _db
        downgrade(alembic_config, "base")


@pytest.fixture(scope="function")
def db_session(db, app):
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()

        _db.session.bind = connection

        yield _db.session

        _db.session.remove()
        transaction.rollback()
        connection.close()


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
