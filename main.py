from catweek.core.context import AppContext
from catweek.db.db_build import create_database_engine
from catweek.db.inserts.db_manip import manipulate_database_menu
from catweek.data import retrieve_database_menu
from catweek.cli import main_menu
def init_context(remote = False, verbose = False):
    engine, metadata = create_database_engine(remote_database=remote)
    return AppContext(
        verbose=verbose,
        remote_database=remote,
        engine=engine,
        metadata=metadata,
    )


if __name__ == "__main__":
    main_menu(init_context())

"""
        elif choice == "1":
            print("\n--- All Tables ---")
            tables = get_tables()
            for table in tables:
                print(table)
            print("--- All Tables ---")

        elif choice == "2":
            print("\n--- Overall Table ---")
            rows = get_overall_table_data()
            for row in rows:
                print(row)
            print("--- Overall Table ---")

        elif choice == "3":
            table = input("Enter table name: ")
            print("\n--- Input Table ---")
            rows = get_table_data(table)
            for row in rows:
                print(row)
            print("--- Input Table ---")

        elif choice == "4":
            group = input("Enter group: ")
            day = input("Enter day: ")
            week = input("Enter week: ")
            print("\n--- Input Schedule ---")
            schedule = get_input_schedule(group, day, week)
            for lesson in schedule:
                print(lesson)
            print("--- Input Schedule ---")

        elif choice == "5":
            print("\n--- Lecturer Schedule ---")
            lecturer_name = input("Enter lecturer name: ")
            schedule = get_lecturer_table_data(lecturer_name)
            for lesson in schedule:
                print(lesson)
            print("--- Lecturer Schedule ---")

        elif choice == "6":
            print("\n--- Connection Test ---")
            success, msg = test_connection()
            if success:
                print(f"success {msg}")
            else:
                print(f"failed {msg}")
            print("--- Connection Test ---")

        else:
            print("\nInvalid option.")
"""