def reset_database(ctx: AppContext):
    print("WARNING: This will delete all data in the database!")
    confirmation = input("Type 'RESET' to confirm: ")

    if confirmation != "RESET":
        print("Aborting reset")
        return

    ctx.metadata.drop_all(ctx.engine)
    ctx.metadata.create_all(ctx.engine)
    print("Database has been reset")