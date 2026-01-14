from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Time, Identity, ForeignKey, CheckConstraint, Boolean
from dotenv import load_dotenv
import os

from sqlalchemy.sql.schema import UniqueConstraint

load_dotenv()

def create_engine_metadata(remote_database: bool = False):

    env_var = 'DATABASE_REMOTE' if remote_database else 'DATABASE_LOCAL'
    database_url = os.getenv(env_var)

    if not database_url:
        raise ValueError(f"{env_var} is not set in .env file")

    engine_test = create_engine(database_url)

    try:
        with engine_test.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise ConnectionError(f"Error connecting to PostgresSQL: {e}")

    metadata_test = MetaData()

    return engine_test, metadata_test

engine, metadata_obj = create_engine_metadata(False)

#Identity(start=1, increment=1) can be used for GENERATED ALWAYS AS IDENTITY
days = Table(
    "days",
    metadata_obj,
    Column("day_id", Integer, Identity(), primary_key=True),
    Column("day_name", String(100), nullable=False)
)

lecturers = Table(
    "lecturers",
    metadata_obj,
    Column("lecturer_id", Integer, Identity(), primary_key=True),
    Column("lecturer_name", String(100), nullable=False, unique=True)
)

lessons = Table(
    "lessons",
    metadata_obj,
    Column("lesson_id", Integer, Identity(), primary_key=True),
    Column("lesson_name", String(100), nullable=False, unique=True),
    Column("lesson_code", String(100), unique=True)
)

times = Table(
    "times",
    metadata_obj,
    Column("time_id", Integer, Identity(), primary_key=True),
    Column("time_start", Time, nullable=False),
    Column("time_end", Time, nullable=False)
)

places = Table(
    "places",
    metadata_obj,
    Column("place_id", Integer, Identity(), primary_key=True),
    Column("cabinet", String(100)),
    Column("url", String(255)),
    Column("lesson_id", Integer, ForeignKey("lessons.lesson_id", ondelete="CASCADE")),
    CheckConstraint(
        "(cabinet IS NOT NULL AND url IS NULL) OR (cabinet IS NULL AND url IS NOT NULL)",
        name="cabinet_or_url_xor"
    )
)

specialties = Table(
    "specialties",
    metadata_obj,
    Column("specialty_id", Integer, Identity(), primary_key=True),
    Column("specialty_name", String(100), nullable=False, unique=True),
    Column("specialty_code", String(10), nullable=False, unique=True)
)

student_groups = Table(
    "student_groups",
    metadata_obj,
    Column("group_id", Integer, Identity(), primary_key=True),
    Column("specialty_id", Integer, ForeignKey("specialties.specialty_id", ondelete="CASCADE")),
    Column("course", Integer, nullable=False),
    Column("group_number", Integer, nullable=False),
    CheckConstraint("course BETWEEN 1 AND 4", name="check_course_range"),
    UniqueConstraint("specialty_id", "course", "group_number")
)

group_presence = Table(
    "group_presence",
    metadata_obj,
    Column("presence_id", Integer, Identity(), primary_key=True),
    Column("group_id", Integer, ForeignKey("student_groups.group_id", ondelete="CASCADE")),
    Column("week_id", Integer, nullable=False),
    Column("is_online", Boolean, nullable=False),
    CheckConstraint("week_id IN (1, 2)", name="check_week_id_range")
)


"""
def lala():
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT day_name, day_id FROM days WHERE day_id = :day_id"), {"day_id": 2})
            for row in result:
                print(f"day: {row.day_name}, id: {row.day_id}")

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")

lala()
"""