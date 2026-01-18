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