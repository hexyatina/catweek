if __name__ == "__main__":
    while True:
        print("\nSelect an option:")
        print("=================")
        print("0. Exit")
        print("1. Get all tables")
        print("2. Get overall table data")
        print("3. Get table data by name")
        print("4. Get schedule for a day and group")
        print("5. Get schedule for Stepanuk")
        print("6. Connection test")
        print("=================")

        choice = input("Enter your choice: ")

        if choice == "0":
            break

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
            print("\n--- Stepanuk Schedule ---")
            schedule = get_Stepanuk_overall_table_data()
            for lesson in schedule:
                print(lesson)
            print("--- Stepanuk Schedule ---")

        elif choice == "6":
            print("\n--- Connection Test ---")
            succes, msg = test_connection()
            if succes:
                print(f"succes {msg}")
            else:
                print(f"failed {msg}")
            print("--- Connection Test ---")

        else:
            print("\nInvalid option.")