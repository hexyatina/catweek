def manipulate_database_menu(ctx: AppContext):
    table_mapping = {
        "days": (insert_days, days),
        "lecturers": (insert_lecturers, lecturers),
        "lessons": (insert_lessons, lessons),
        "times": (insert_times, times),
        "places": (insert_places, places),
        "specialties": (insert_specialties, specialties),
        "student_groups": (insert_student_groups, student_groups),
        "group_presence": (insert_group_presence, group_presence),
        # "overall_schedule": (insert_overall_schedule, overall_schedule),
    }

    while True:
        print("\n" + "=" * 40)
        print("DATABASE MANIPULATION")
        print("=" * 40)
        print("0. Back to Main Menu")
        print("1. Reset Database (drop and recreate tables)")
        print(f"2. Insert All Data (HARDCODED) [Verbose: {'ON' if ctx.verbose else 'OFF'}]")
        print(f"3. Insert Data (HARDCODED) by Table Name [Verbose: {'ON' if ctx.verbose else 'OFF'}]")
        print("4. List Available for HARDCODED INSERT Tables")
        print("5. Clear Specific table (delete all data)")
        print("=" * 40)
        print(f"v. Toggle Verbose (Currently {'ON' if ctx.verbose else 'OFF'})")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            reset_database(ctx)
            input("Press enter to continue...")
        elif choice == "2":
            insert_all_data(ctx)
            input("Press enter to continue...")
        elif choice == "3":
            table_name = input("Enter table name: ").strip()
            insert_specific_table(table_name, ctx, table_mapping)
            input("Press enter to continue...")
        elif choice == "4":
            print("\nAvailable tables for data insertion:")
            print("-" * 40)
            for i, table_name in enumerate(table_mapping.keys(), 1):
                print(f"{i}. {table_name}")
            print("-" * 40)
            input("Press enter to continue...")
        elif choice == "v":
            ctx.verbose = not ctx.verbose
            print(f"Verbose: {'ON' if ctx.verbose else 'OFF'}")
        elif choice == "5":
            table_name = input("Enter table name to clear: ").strip()
            clear_specific_table(table_name, ctx)
            input("Press enter to continue...")
        else:
            print("Invalid choice")

if __name__ == '__main__':
    manipulate_database_menu(ctx=AppContext())