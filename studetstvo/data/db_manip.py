from sqlalchemy import insert, text
from .models import ( engine, metadata_obj, days, lecturers,
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

days_insert = (insert
               (days),
               [
                   {"day_name": "Понеділок"},
                   {"day_name": "Вівторок"},
                   {"day_name": "Середа"},
                   {"day_name": "Четвер"},
                   {"day_name": "П'ятниця"},
               ],
)

lecturers_insert = (insert
                    (lecturers),
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
                    ],
)

lessons_insert = (insert
                  (lessons),
                  [
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
                  ],
)

times_insert = (insert
                (times),
                [
                    {"time_start": "09:00:00", "time_end": "10:20:00"},
                    {"time_start": "10:30:00", "time_end": "11:50:00"},
                    {"time_start": "12:10:00", "time_end": "13:30:00"},
                    {"time_start": "13:40:00", "time_end": "15:00:00"},
                    {"time_start": "15:10:00", "time_end": "16:30:00"},
                ],
)

cabinet_insert = (insert
                 (places),
                 [
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
                 ],
)

url_insert = (insert
                 (places),
                 [
                     {"url": ""}
                 ])

def fill_db():
    with engine.begin() as conn:


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
