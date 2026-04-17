import time
from sqlalchemy import text, create_engine
from ..extensions import db
from ..models import Base, Day, Slot, Venue, Lecturer, Lesson, Specialty, StudentGroup
from ..data import DAYS, SLOTS, VENUES, LECTURERS, LESSONS, SPECIALTIES, STUDENT_GROUPS
from flask_migrate import upgrade
from ..config import settings

class DatabaseService:

    @staticmethod
    def _direct_engine():
        return create_engine(settings.get_database_url(direct=True))

    @staticmethod
    def test_connection():
        masked_url = settings.get_database_url(direct=True).split("@")[-1]

        print(f"DEBUG: Attempting to connect to {masked_url}")

        while True:
            try:
                engine = DatabaseService._direct_engine()
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("DEBUG: Connection successful")
                break
            except Exception as e:
                print(f"Database not reachable: {e}")
                print("Retrying in 3 seconds...")
                time.sleep(3)

    @staticmethod
    def reset_content():
        with db.engine.connect() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(table.delete())
            conn.commit()

    @staticmethod
    def reset_db_schema():
        engine = DatabaseService._direct_engine()

        with engine.begin() as conn:
            conn.execute(text("DROP SCHEMA IF EXISTS schedule CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS public.alembic_version"))
            conn.execute(text("CREATE SCHEMA schedule"))

        upgrade()

    @staticmethod
    def seed_system_data():
        try:
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
        except Exception as e:
            db.session.rollback()
            print(f"Seed failed with {e}")
            raise e