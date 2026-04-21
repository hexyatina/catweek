import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text

TEST_DATABASE_LOCAL = os.environ.get(
    "TEST_DATABASE_LOCAL",
    "postgresql+psycopg://postgres:1845@localhost:5432/test_catweek"
)

os.environ.setdefault("APP_ENV", "dev")
os.environ.setdefault("DB_ENV", "local")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ["DATABASE_LOCAL"] = TEST_DATABASE_LOCAL


@pytest.fixture(scope="session")
def app():
    from src.app import create_app

    flask_app = create_app()
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_LOCAL

    yield flask_app


@pytest.fixture(scope="module")
def alembic_config(app):
    cfg = Config("alembic.ini")
    cfg.set_main_option("script_location", "migrations")
    cfg.set_main_option(
        "sqlalchemy.url",
        app.config["SQLALCHEMY_DATABASE_URI"].replace("%", "%%")
    )

    return cfg


@pytest.fixture(scope="module", autouse=True)
def db_tables(app, alembic_config):
    from src.app.extensions import db
    with app.app_context():
        db.session.execute(text("DROP SCHEMA IF EXISTS schedule CASCADE"))
        db.session.execute(text("CREATE SCHEMA schedule"))
        db.session.commit()

        command.upgrade(alembic_config, "head")

        yield

        db.session.remove()


@pytest.fixture()
def db_session(app, db_tables):
    from src.app.extensions import db as _db

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
def auth_header():
    return {"X-Api-Key": os.environ["API_KEY"]}
