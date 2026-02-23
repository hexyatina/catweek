from sqlalchemy import schema, inspect, text
from ..extensions import db
from ..models import *
from ..data import *
from ..utils import parse_time_slot
from flask_migrate import upgrade

class DatabaseService:

    @staticmethod
    def reset_content():
        for table in reversed(Base.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    @staticmethod
    def reset_db_schema(app):
        target_schema = Base.metadata.schema

        with db.engine.connect() as conn:
            conn.execute(schema.DropSchema(target_schema, cascade=True, if_exists=True))
            conn.execute(text("DROP TABLE IF EXISTS public.alembic_version"))
            conn.commit()

        with app.app_context():

            inspector = inspect(db.engine)
            if target_schema not in inspector.get_schema_names():
                with db.engine.connect() as conn:
                        conn.execute(schema.CreateSchema(target_schema))
                        conn.commit()

            upgrade()

    @staticmethod
    def seed_system_data():
        db.session.add_all([Day(**d) for d in DAYS])
        db.session.add_all([Venue(**v) for v in VENUES])
        db.session.add_all([Lecturer(**lec) for lec in LECTURERS])
        db.session.add_all([Lesson(**l) for l in LESSONS])

        db.session.add_all([
            Slot(time_start=start_slot, time_end=end_slot)
            for start_slot, end_slot in (parse_time_slot(s_str) for s_str in SLOTS)
        ])

        spec_map = {}
        for s_data in SPECIALTIES:
            spec = Specialty(**s_data)
            db.session.add(spec)
            spec_map[s_data["code"]] = spec

        db.session.flush()

        for g_data in STUDENT_GROUPS:
            code = g_data["specialty_code"]
            if code in spec_map:
                db.session.add(StudentGroup(
                    specialty_id=spec_map[code].id,
                    course=g_data["course"],
                    group_number=g_data["group_number"],
                )
                )
        db.session.commit()