from sqlalchemy import insert

def insert_simple(conn, table, rows):
    conn.execute(insert(table), rows)

from catweek.db import days, lecturers, lessons, times, places, specialties
from catweek.data import DAYS, LECTURERS, LESSONS, TIMES, CABINETS, URLS, SPECIALTIES, STUDENT_GROUPS, GROUP_PRESENCE
from .base import insert_simple, insert_urls, insert_student_groups, insert_group_presence

SIMPLE_INSERTS = [
    (days, DAYS),
    (lecturers, LECTURERS),
    (lessons, LESSONS),
    (times, TIMES),
    (places, CABINETS),
    (specialties, SPECIALTIES),
]


def insert_all_initial(conn):
    for table, rows in SIMPLE_INSERTS:
        insert_simple(conn, table, rows)

    insert_urls(conn, URLS)
    insert_student_groups(conn, STUDENT_GROUPS)
    insert_group_presence(conn, GROUP_PRESENCE)



def insert_all_data(ctx: AppContext):
    print("Are you sure you want to fill the database with all data?")
    if input("[Y/N]: ") != "Y":
        print("Aborting")
        return

    with ctx.engine.begin() as conn:
        try:
            insert_days(conn)
            if ctx.verbose:
                print("\n--- Days Table ---")
                rows = conn.execute(select(days)).fetchall()
                for row in rows:
                    print(row)
                print("--- Days Table ---")

            insert_lecturers(conn)
            if ctx.verbose:
                print("\n--- Lecturers Table ---")
                rows = conn.execute(select(lecturers)).fetchall()
                for row in rows:
                    print(row)
                print("--- Lecturers Table ---")

            insert_lessons(conn)
            if ctx.verbose:
                print("\n--- Lessons Table ---")
                rows = conn.execute(select(lessons)).fetchall()
                for row in rows:
                    print(row)
                print("--- Lessons Table ---")

            insert_times(conn)
            if ctx.verbose:
                print("\n--- Times Table ---")
                rows = conn.execute(select(times)).fetchall()
                for row in rows:
                    print(row)
                print("--- Times Table ---")

            insert_places(conn)
            if ctx.verbose:
                print("\n--- Places Table ---")
                rows = conn.execute(select(places)).fetchall()
                for row in rows:
                    print(row)
                print("--- Places Table ---")

            insert_specialties(conn)
            if ctx.verbose:
                print("\n--- Specialties Table ---")
                rows = conn.execute(select(specialties)).fetchall()
                for row in rows:
                    print(row)
                print("--- Specialties Table ---")

            insert_student_groups(conn)
            if ctx.verbose:
                print("\n--- Student Groups Table ---")
                rows = conn.execute(select(student_groups)).fetchall()
                for row in rows:
                    print(row)
                print("--- Student Groups Table ---")

            insert_group_presence(conn)
            if ctx.verbose:
                print("\n--- Group Presence Table ---")
                rows = conn.execute(select(group_presence)).fetchall()
                for row in rows:
                    print(row)
                print("--- Group Presence Table ---")

            print("\nDatabase has been filled successfully")
        except Exception as e:
            print(f"Error filling database: {e}")
            raise

def insert_specific_table(table_name, ctx: AppContext, available_inserts):

    if table_name not in available_inserts:
        print(f"Table not in standard insert_functions list: {table_name}")
        return

    insert_func, table_obj = available_inserts[table_name]

    with ctx.engine.begin() as conn:
        try:
            insert_func(conn)

            if ctx.verbose:
                print(f"\n--- {table_name} Table ---")
                rows = conn.execute(select(table_obj)).fetchall()
                for row in rows:
                    print(row)
                print(f"--- {table_name} Table ---")

            print(f"\nData inserted into '{table_name}' successfully")
        except Exception as e:
            print(f"Error inserting data: {e}")

def clear_specific_table(table_name, ctx: AppContext):
    table_mapping = {
        "days": days,
        "lecturers": lecturers,
        "lessons": lessons,
        "times": times,
        "places": places,
        "specialties": specialties,
        "student_groups": student_groups,
        "group_presence": group_presence,
        "overall_schedule": overall_schedule,
    }

    if table_name not in table_mapping:
        print(f"Unknown table: {table_name}")
        return

    print(f"WARNING: This will delete all data from '{table_name}' table!")
    confirmation = input("Type 'DELETE' to confirm: ")
    if confirmation != "DELETE":
        print("Aborting")
        return

    table_obj = table_mapping[table_name]

    with ctx.engine.begin() as conn:
        try:
            conn.execute(table_obj.delete())
            print(f"\n--- {table_name} table cleared ---")
        except Exception as e:
            print(f"Error dropping table data: {e}")


"""
def add_user_column(table_name):
    try:

        with engine.connect() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN user_id INT"))

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []

"""