from sqlalchemy import create_engine, text

from sqlalchemy import MetaData
from dotenv import load_dotenv
import os

load_dotenv()

def create_engine_metadata(remote_database: bool = False):

    env_var = 'DATABASE_REMOTE' if remote_database else 'DATABASE_LOCAL'
    database_url = os.getenv(env_var)

    if not database_url:
        raise ValueError(f"{env_var} is not set in .env file")

    db_engine = create_engine(database_url)

    try:
        with db_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise ConnectionError(f"Error connecting to PostgresSQL: {e}")

    metadata = MetaData()

    return db_engine, metadata

def get_tables():
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:
            return connection.execute(text("SELECT table_name FROM information_schema.tables WHERE "
                                           "table_schema='public'")).fetchall()
    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []


def get_table_data(table_name):
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:

            table_data = connection.execute(text(f"SELECT * FROM {table_name}"))
            table_data = [dict(row._mapping) for row in table_data]
            return table_data

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []


def get_overall_table_data():
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:

            query = text("""
                SELECT t.timestart, t.timeend, g.groupname, l.lessonname, 
                    d.dayname, d.weekid, lec.lecturername, p.cabinet, p.url
                FROM overall o 
                JOIN times t ON o.lessontime = t.timeid
                JOIN ipz_groups g ON o.groupnames = g.groupid
                JOIN lessons l ON o.lesson = l.lessonid
                JOIN days d ON o.dayname = d.dayid
                JOIN lecturers lec ON o.lecturer = lec.lecturerid
                JOIN places p ON o.place = p.placeid
            """)

            overall_data = connection.execute(query)
            overall_data = [dict(row._mapping) for row in overall_data]
            return overall_data

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []


def get_input_schedule(group, day, week):
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:

            query = text("""
                SELECT t.timestart, t.timeend, 
                       l.lessonname, lec.lecturername, 
                       p.cabinet, p.url
                FROM overall o 
                    JOIN times t ON o.lessontime = t.timeid
                    JOIN lessons l ON o.lesson = l.lessonid
                    JOIN lecturers lec ON o.lecturer = lec.lecturerid
                    JOIN places p ON o.place = p.placeid
                    JOIN days d ON o.dayname = d.dayid
                    JOIN ipz_groups g ON o.groupnames = g.groupid
                WHERE d.dayname = :day AND g.groupname = :group AND d.weekid = :week
                ORDER BY t.timestart
            """)

            day_data = connection.execute(query, {"group": group, "day": day, "week": week})
            day_data = [dict(row._mapping) for row in day_data]
            return day_data

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return []

def get_lecturer_table_data(lecturer_name):
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:

            query = text("""
                         SELECT t.timestart,
                                t.timeend,
                                g.groupname,
                                l.lessonname,
                                d.dayname,
                                d.weekid,
                                p.cabinet,
                                p.url
                         FROM overall o
                                  JOIN times t ON o.lessontime = t.timeid
                                  JOIN ipz_groups g ON o.groupnames = g.groupid
                                  JOIN lessons l ON o.lesson = l.lessonid
                                  JOIN days d ON o.dayname = d.dayid
                                  JOIN lecturers lec ON o.lecturer = lec.lecturerid
                                  JOIN places p ON o.place = p.placeid
                         WHERE lec.lecturername = :lecturer
                         ORDER BY t.timestart
                         """)

            lecturer_table_data = connection.execute(query, {"lecturer": lecturer_name})
            lecturer_table_data = [dict(row._mapping) for row in lecturer_table_data]
            return lecturer_table_data

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []
