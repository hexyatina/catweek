from sqlalchemy import insert, text, select, literal, union_all
from studetstvo.data.models import ( engine, metadata_obj, days, lecturers,
                      lessons, times, places, specialties,
                      student_groups, group_presence, overall_schedule
)

def reset_db():
    print("Are you sure you want to reset the database?")
    if input("[Y/N]:") != "Y":
        print("Aborting")
        return
    else:
        with engine.begin() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
        metadata_obj.create_all(engine)
        print("Database has been reset")


def insert_days(conn):
    conn.execute(
        insert(days),
        [
            {"day_name": "Понеділок"},
            {"day_name": "Вівторок"},
            {"day_name": "Середа"},
            {"day_name": "Четвер"},
            {"day_name": "П'ятниця"},
        ]
    )

def insert_lecturers(conn):
    conn.execute(
        insert(lecturers),
        [
            {"lecturer_name": "Затула"},
            {"lecturer_name": "Капічина"},
            {"lecturer_name": "Степанюк"},
            {"lecturer_name": "Ходжаєв"},
            {"lecturer_name": "Головай"},
            {"lecturer_name": "Руденко"},
            {"lecturer_name": "Тільга"},
            {"lecturer_name": "Таран"},
            {"lecturer_name": "Мироненко"},
            {"lecturer_name": "Герасимович"},
            {"lecturer_name": "Гаращенкo"},
            {"lecturer_name": "Коваль"},
        ]
    )

def
lessons_values = [
    {"lesson_name": "Математичний аналіз", "lesson_code": "Матан"},
    {"lesson_name": "Лінійна алгебра", "lesson_code": "Лінійка"},
    {"lesson_name": "Інженерія програмного забезпечення", "lesson_code": "ІПЗ"},
    {"lesson_name": "Сервіси та середовище розробки програмного забезпечення", "lesson_code": "РПЗ"},
    {"lesson_name": "Українська мова", "lesson_code": "Укр"},
    {"lesson_name": "Англійська мова", "lesson_code": "Англ"},
    {"lesson_name": "Французька мова", "lesson_code": "Фран"},
    {"lesson_name": "Основи програмування та алгоритмічні мови", "lesson_code": "ОПАМ"},
    {"lesson_name": "Фізичне виховання", "lesson_code": "Фізра"},
    {"lesson_name": "Архітектура комп'ютера і комп'ютерна схемотехніка", "lesson_code": "АККС"},
    {"lesson_name": "Теорія ймовірності", "lesson_code": "Ймовірності"},
    {"lesson_name": "Дискретна математика", "lesson_code": "Дискретка"},
]
lessons_insert = insert(lessons)


times_values = [
    {"time_start": "09:00:00", "time_end": "10:20:00"},
    {"time_start": "10:30:00", "time_end": "11:50:00"},
    {"time_start": "12:10:00", "time_end": "13:30:00"},
    {"time_start": "13:40:00", "time_end": "15:00:00"},
    {"time_start": "15:10:00", "time_end": "16:30:00"},
]
times_insert = insert(times)


cabinet_values = [
    {"cabinet": "10"},
    {"cabinet": "14"},
    {"cabinet": "20"},
    {"cabinet": "25"},
    {"cabinet": "26"},
    {"cabinet": "30"},
    {"cabinet": "31"},
    {"cabinet": "34"},
    {"cabinet": "35"},
    {"cabinet": "37"},
    {"cabinet": "39"},
    {"cabinet": "41"},
    {"cabinet": "C3"},
]
cabinet_insert = insert(places)


url_values = [
    {"url": "...", "place_id": "..."},
]
url_insert = insert(places)


specialties_values = [
    {"specialty_name": "Інженерія Програмного Забезпечення", "specialty_code": "ІПЗ"},
]
specialties_insert = insert(specialties)


spec = (
    select(specialties.c.specialty_id)
    .where("ІПЗ" == specialties.c.specialty_code)
    .cte("spec")
)

student_groups_values = (union_all(
        select(
            literal(3).label("course"),
            literal(1).label("group_number")
        ),
        select(
            literal(3),
            literal(2)
        ),
        select(
            literal(3),
            literal(3)
        )
    )
    .cte("student_groups_insert_values")
)

student_groups_insert = insert(student_groups).from_select(
    ["specialty_id", "course", "group_number"],
    select(
        spec.c.specialty_id,
        student_groups_values.c.course,
        student_groups_values.c.group_number
    )
)


target_groups = (
    select(
        student_groups.c.group_id,
        student_groups.c.group_number
    )
    .join(specialties)
    .where(
        "ІПЗ" == specialties.c.specialty_code,
        3 == student_groups.c.course
    )
    .cte("target_groups")
)

week_rows = (union_all(
        select(
            literal(1).label("week_id"),
            literal(True).label("is_online")
        ),
        select(
            literal(2),
            literal(False)
        )
    )
    .cte("week_rows")
)

group_presence_insert = insert(group_presence).from_select(
    ["group_id", "week_id", "is_online"],
    select(
        target_groups.c.group_id,
        week_rows.c.week_id,
        week_rows.c.is_online
    )
    .where(
        target_groups.c.group_number.in_([1, 2, 3])
    )
)



def fill_db():
    with engine.begin() as conn:
        conn.execute(days_insert, days_values)
        conn.execute(lecturers_insert, lecturers_values)
        conn.execute(lessons_insert, lessons_values)
        conn.execute(times_insert, times_values)
        conn.execute(cabinet_insert, cabinet_values)
        conn.execute(url_insert, url_values)
        conn.execute(specialties_insert, specialties_values)
        conn.execute(student_groups_insert)
        conn.execute(group_presence_insert)


"""
def get_tables():
    try:

        with engine.connect() as connection:
            return connection.execute(text("SELECT table_name FROM information_schema.tables WHERE "
                                           "table_schema='public'")).fetchall()

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []

def get_table_data(table_name):
    try:

        with engine.connect() as connection:

            table_data = connection.execute(text(f"SELECT * FROM {table_name}"))
            table_data = [dict(row._mapping) for row in table_data]
            return table_data

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []

def add_user_column(table_name):
    try:

        with engine.connect() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN user_id INT"))

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []


reset_db()
"""