from studetstvo.context import AppContext
from sqlalchemy import inspect


"""
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

            query = text(
                SELECT t.timestart, t.timeend, g.groupname, l.lessonname, 
                    d.dayname, d.weekid, lec.lecturername, p.cabinet, p.url
                FROM overall o 
                JOIN times t ON o.lessontime = t.timeid
                JOIN ipz_groups g ON o.groupnames = g.groupid
                JOIN lessons l ON o.lesson = l.lessonid
                JOIN days d ON o.dayname = d.dayid
                JOIN lecturers lec ON o.lecturer = lec.lecturerid
                JOIN places p ON o.place = p.placeid
            )

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

            query = text(
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
            )

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

            query = text(
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
                         )

            lecturer_table_data = connection.execute(query, {"lecturer": lecturer_name})
            lecturer_table_data = [dict(row._mapping) for row in lecturer_table_data]
            return lecturer_table_data

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []
"""

def return_metadata_tables(ctx: AppContext):
    tables = ctx.metadata.tables
    return tables

def return_existing_tables(ctx: AppContext):
    inspector = inspect(ctx.engine)
    tables = inspector.get_table_names()
    return tables

def retrieve_database_menu(ctx: AppContext):

    while True:
        print("\n" + "=" * 40)
        print("DATABASE RETRIEVER")
        print("=" * 40)
        print("0. Back to Main Menu")
        print("1. Print all tables in metadata (created via python)")
        print("2. Print all tables existing in database")
        print("3. SELECT table")
        print("4. SELECT table with JOIN")
        print("5. SELECT all tables")
        print("6. GET schedule")
        print("7. GET schedule by table")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            result = return_metadata_tables(ctx)
            if not result:
                print("No tables found in metadata")
            else:
                print(f"{"\n" + "-" * 20}Metadata Tables{"-" * 20}")
                for table in result:
                    print(table)
                print(f"{"-" * 20}Metadata Tables{"-" * 20}")
            input("Press enter to continue...")

        elif choice == "2":
            result = return_existing_tables(ctx)
            if not result:
                print("No tables found in database")
            else:
                print(f"{"\n" + "-" * 20}Database Tables{"-" * 20}")
                for table in result:
                    print(table)
                print(f"{"-" * 20}Database Tables{"-" * 20}")
            input("Press enter to continue...")
        elif choice == "3":
            table_name = input("Enter table name: ").strip()
            #insert_specific_table(table_name, verbose=verbose)
        elif choice == "4":
            print("\nAvailable tables for data insertion:")
        elif choice == "5":
            pass
        elif choice == "6":
            table_name = input("Enter table name to clear: ").strip()
            #clear_specific_table(table_name)
        else:
            print("Invalid choice")
