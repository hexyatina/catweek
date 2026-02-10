def reset_database(ctx: AppContext):
    print("WARNING: This will delete all data in the database!")
    confirmation = input("Type 'RESET' to confirm: ")

    if confirmation != "RESET":
        print("Aborting reset")
        return

    ctx.metadata.drop_all(ctx.engine)
    ctx.metadata.create_all(ctx.engine)
    print("Database has been reset")

    from catweek.core.context import AppContext
    from sqlalchemy import inspect

    """
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

                query = 
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


    def return_metadata_tables(ctx: AppContext):
        tables = ctx.metadata.tables
        return tables

    def return_existing_tables(ctx: AppContext):
        inspector = inspect(ctx.engine)
        tables = inspector.get_table_names()
        return tables
    """