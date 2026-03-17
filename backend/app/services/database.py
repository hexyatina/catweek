from sqlalchemy import schema, inspect, text, create_engine
from ..extensions import db
from ..models import Base, Day, Slot, Venue, Lecturer, Lesson, Specialty, StudentGroup
from ..data import DAYS, SLOTS, VENUES, LECTURERS, LESSONS, SPECIALTIES, STUDENT_GROUPS
from flask_migrate import upgrade


class DatabaseService:

    @staticmethod
    def _direct_engine():
        from ..config import settings
        return create_engine(settings.DATABASE_URL_DIRECT)

    @staticmethod
    def reset_content():
        with db.engine.connect() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(table.delete())
            conn.commit()

    @staticmethod
    def reset_db_schema(app):
        target_schema = Base.metadata.schema
        engine = DatabaseService._direct_engine()

        with db.engine.connect() as conn:
            conn.execute(schema.DropSchema(target_schema, cascade=True, if_exists=True))
            conn.execute(text("DROP TABLE IF EXISTS public.alembic_version"))
            conn.commit()

        inspector = inspect(db.engine)
        if target_schema not in inspector.get_schema_names():
            with db.engine.connect() as conn:
                conn.execute(schema.CreateSchema(target_schema))
                conn.commit()

        upgrade()

    @staticmethod
    def seed_system_data():
        db.session.add_all([Day(**d) for d in DAYS])
        db.session.add_all([Slot(**s) for s in SLOTS])
        db.session.add_all([Venue(**v) for v in VENUES])
        db.session.add_all([Lecturer(**lec) for lec in LECTURERS])
        db.session.add_all([Lesson(**l) for l in LESSONS])

        spec_map = {}
        for s_data in SPECIALTIES:
            spec = Specialty(**s_data)
            db.session.add(spec)
            spec_map[s_data["code"]] = spec

        db.session.flush()

        for g_data in STUDENT_GROUPS:
            spec = spec_map.get(g_data["specialty_code"])
            if spec is None:
                raise ValueError(f"Unknown specialty: {g_data['specialty_code']}")
            db.session.add(StudentGroup(
                specialty_id=spec.id,
                course=g_data["course"],
                group_number=g_data["group_number"],
            ))

        db.session.commit()