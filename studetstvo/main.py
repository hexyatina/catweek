from context import AppContext
from studetstvo.data.models import create_database_engine
from studetstvo.data.db_manip import manipulate_database_menu
from studetstvo.data.database import retrieve_database_menu

def init_context(remote = False, verbose = False):
    engine, metadata = create_database_engine(remote_database=remote)
    return AppContext(
        verbose=verbose,
        remote_database=remote,
        engine=engine,
        metadata=metadata,
    )


def main_terminal():
    ctx = init_context()
    ctx.metadata.create_all(ctx.engine)
    while True:
        print("\n" + "=" * 40)
        print("MAIN MENU")
        print("=" * 40)
        print("0. Exit")
        print("1. Manipulate Database")
        print("2. Retrieve Database")
        print("=" * 40)
        print(f"v. Toggle Verbose (Currently {'ON' if ctx.verbose else 'OFF'})")
        print(f"s. Toggle LOCAL / REMOTE databases (Currently {'REMOTE' if ctx.remote_database else 'LOCAL'})")
        print("=" * 40)

        cmd = input("Enter your choice: ").strip()

        match cmd:
            case "0":
                print("Exit")
                break
            case "1":
                manipulate_database_menu(ctx)
            case "2":
                retrieve_database_menu(ctx)
            case "v":
                ctx.verbose = not ctx.verbose
                print(f"Verbose: {'ON' if ctx.verbose else 'OFF'}")
            case "s":
                ctx.remote_database = not ctx.remote_database
                print(f"DATABASE: {'REMOTE' if ctx.remote_database else 'LOCAL'}")
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    main_terminal()

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