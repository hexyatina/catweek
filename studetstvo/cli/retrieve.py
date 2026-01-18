def retrieve_database_menu(ctx: AppContext):

    while True:
        print("\n" + "=" * 40)
        print("DATABASE RETRIEVER")
        print("=" * 40)
        print("0. Back to Main Menu")
        print("1. Print all tables in metadata (created via python)")
        print("2. Print all tables existing in database")
        #print("3. SELECT table")
        #print("4. SELECT table with JOIN")
        #print("5. SELECT all tables")
        #print("6. GET schedule")
        #print("7. GET schedule by table")
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