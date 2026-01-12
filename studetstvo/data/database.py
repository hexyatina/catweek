from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()

REMOTE_DATABASE = False

if REMOTE_DATABASE:
    #for remote database using neon console
    DATABASE = os.getenv('DATABASE_URL')
    if DATABASE and "+psycopg" not in DATABASE:
        DATABASE = DATABASE.replace("postgresql://", "postgresql+psycopg://")
else:
    #for local database
    DATABASE = "postgresql+psycopg://postgres:1845@localhost:5432/postgres"

def test_connection():
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True, "Connection successful!"
    except Exception as e:
        return False, str(e)

def get_tables():
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:
            return connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()

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
        print(f"Error connecting to PostgreSQL: {e}")
        return []


def get_input_schedule(group, day, week):
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:

            query = text("""
                SELECT t.timestart, t.timeend, l.lessonname, lec.lecturername, p.cabinet, p.url
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
"""
@app.route('/api/schedule/<group_name>')
def get_schedule(group_name):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''SELECT t.timestart,
                       t.timeend,
                       g.groupname,
                       l.lessonname,
                       d.dayname,
                       lec.lecturername,
                       p.cabinet,
                       p.url
                FROM overall o
                         JOIN times t ON o.lessontime = t.timeid
                         JOIN ipz_groups g ON o.groupnames = g.groupid
                         JOIN lessons l ON o.lesson = l.lessonid
                         JOIN days d ON o.dayname = d.dayid
                         JOIN lecturers lec ON o.lecturer = lec.lecturerid
                         JOIN places p ON o.place = p.placeid
                WHERE g.groupname = %s
                ORDER BY d.dayid, t.timeid''', (group_name,))

    schedule = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(schedule)
"""

def get_Stepanuk_overall_table_data():
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:

            query = text("""
                SELECT t.timestart, t.timeend, g.groupname, l.lessonname, 
                    d.dayname, d.weekid, p.cabinet, p.url
                FROM overall o 
                JOIN times t ON o.lessontime = t.timeid
                JOIN ipz_groups g ON o.groupnames = g.groupid
                JOIN lessons l ON o.lesson = l.lessonid
                JOIN days d ON o.dayname = d.dayid
                JOIN lecturers lec ON o.lecturer = lec.lecturerid
                JOIN places p ON o.place = p.placeid
                WHERE  lec.lecturerid = 103
            """)

            day_data = connection.execute(query)
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
                SELECT t.timestart, t.timeend, l.lessonname, lec.lecturername, p.cabinet, p.url
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

            cur.execute('''SELECT t.timestart,
                                  t.timeend,
                                  g.groupname,
                                  l.lessonname,
                                  d.dayname,
                                  lec.lecturername,
                                  p.cabinet,
                                  p.url
                           FROM overall o
                                    JOIN times t ON o.lessontime = t.timeid
                                    JOIN ipz_groups g ON o.groupnames = g.groupid
                                    JOIN lessons l ON o.lesson = l.lessonid
                                    JOIN days d ON o.dayname = d.dayid
                                    JOIN lecturers lec ON o.lecturer = lec.lecturerid
                                    JOIN places p ON o.place = p.placeid
                           WHERE g.groupname = %s
                           ORDER BY d.dayid, t.timeid''', (group_name,))

            data = connection.execute(query, {"group": group, "day": day, "week": week})
            data = [dict(row._mapping) for row in day_data]
            return day_data

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return []