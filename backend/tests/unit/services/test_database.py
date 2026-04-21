from alembic import command

from sqlalchemy import text

TEST_DATABASE_LOCAL = None


def test_migrations_upgrade_to_head(app, alembic_config):
    from src.app.extensions import db

    with app.app_context():
        db.drop_all()

        command.upgrade(alembic_config, "head")


def test_migrations_create_table(app, db_tables):
    from src.app.extensions import db
    from sqlalchemy import inspect

    with app.app_context():
        inspector = inspect(db.engine)
        existing = set(inspector.get_table_names(schema="schedule"))

    expected = {
        "specialties", "student_groups", "days",
        "schedules", "lecturers", "lessons", "slots", "venues",
    }
    missing = expected - existing
    assert not missing, f"Missing tables: {missing}"


def test_migrations_upgrade_is_idempotent(app, alembic_config):
    with app.app_context():
        command.upgrade(alembic_config, "head")


def test_alembic_version_table_exists(app):
    from src.app.extensions import db

    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(
                text("SELECT version_num FROM alembic_version LIMIT 1")
            ).fetchone()
            assert result is not None, "alembic_version is empty — migrations may not have run"
