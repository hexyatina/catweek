from sqlalchemy import insert, select, literal, union_all, true
from catweek.core.context import AppContext
from catweek.db.db_build import (days, lecturers,
                                 lessons, times, places, specialties,
                                 student_groups, group_presence, overall_schedule
                                 )




    url_entries = [
        {"lesson_code": "АККС", "url": "https://us05web.zoom.us/j/89525632789?pwd=lvsjsxPulwqMMtIbB5yWCYP4ayMtUW"},
    ]

    for entry in url_entries:
        lesson_id = conn.execute(
            select(lessons.c.lesson_id)
            .where(entry["lesson_code"] == lessons.c.lesson_code)
        ).scalar_one()

        conn.execute(
            insert(places),
            [{"lesson_id": lesson_id, "url": entry["url"]}]
        )

def insert_specialties(conn):
    conn.execute(
        insert(specialties),
        [
            # {"specialty_name": "Інженерія Програмного Забезпечення", "specialty_code": "ІПЗ"},
        ]
    )

def insert_student_groups(conn):

    specialty_id = conn.execute(
        select(
            specialties.c.specialty_id
        ).where(
            "ІПЗ" == specialties.c.specialty_code
        )
    ).scalar_one()

    rows = [
        {"specialty_id": specialty_id, "course": 3, "group_number": 1},
        {"specialty_id": specialty_id, "course": 3, "group_number": 2},
        {"specialty_id": specialty_id, "course": 3, "group_number": 3},
    ]

    conn.execute(insert(student_groups), rows)

def insert_group_presence(conn):

    target_groups = (
        select(
            student_groups.c.group_id,
            student_groups.c.group_number
        )
        .join(specialties)
        .where(
            specialties.c.specialty_code == "ІПЗ",
            student_groups.c.course == 3
        )
        .cte("target_groups")
    )


    week_rows = (
        union_all(
            select(
                literal(1).label("week_id"),
                literal(True).label("is_online")
            ),
            select(
                literal(2),
                literal(False)
            ),
        )
        .cte("week_rows")
    )

    stmt = insert(group_presence).from_select(
        ["group_id", "week_id", "is_online"],
        select(
            target_groups.c.group_id,
            week_rows.c.week_id,
            week_rows.c.is_online
        )
        .select_from(
            target_groups.join(week_rows, true())
        )
        .where(
            target_groups.c.group_number.in_([1, 2, 3])
        )
    )

    conn.execute(stmt)

def insert_overall_schedule(conn,
                            *,
                            days: list[str], lecturers: list[str], lessons: list[str], times: list[str], places: list[str | None], specialties_code: str, course: int, group_numbers: list[str], weeks: list[tuple[int, bool]], ):

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