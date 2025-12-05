from sqlalchemy import create_engine, text

DATABASE_URI = "postgresql+psycopg://postgres:1845@localhost:5432/postgres"

def get_tables():
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:
            return connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return []


def get_table_data(table_name):
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:

            table_data = connection.execute(text(f"SELECT * FROM {table_name}"))
            table_data = [dict(row._mapping) for row in table_data]
            return table_data

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return []


def get_overall_table_data():
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:

            query = text("""
                SELECT t.timestart, t.timeend, g.groupname, l.lessonname, 
                    d.dayname, d.weekid, lec.lecturername, p.cabinet, p.url
                FROM overall o 
                JOIN times t ON o.lessontime = t.timeid
                JOIN ipz_groups g ON o.groupnames = g.groupid
                JOIN lessons l ON o.lesson = l.lessonid
                JOIN days d ON o.dayname = d.dayid
                JOIN lecturers lec ON o.lecturer = lec.lecturerid
                JOIN places p ON o.place = p.placeid
            """)

            overall_data = connection.execute(query)
            overall_data = [dict(row._mapping) for row in overall_data]
            return overall_data

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return []


def get_input_schedule(group, day, week):
    try:
        engine = create_engine(DATABASE_URI)
        with engine.connect() as connection:

            query = text("""
                SELECT t.timestart, t.timeend, l.lessonname, lec.lecturername, p.cabinet, p.url
                FROM overall o 
                JOIN times t ON o.lessontime = t.timeid
                JOIN lessons l ON o.lesson = l.lessonid
                JOIN lecturers lec ON o.lecturer = lec.lecturerid
                JOIN places p ON o.place = p.placeid
                JOIN days d ON o.dayname = d.dayid
                JOIN ipz_groups g ON o.groupnames = g.groupid
                WHERE d.dayname = :day AND g.groupname = :group AND d.weekid = :week
                ORDER BY t.timestart
            """)

            day_data = connection.execute(query, {"group": group, "day": day, "week": week})
            day_data = [dict(row._mapping) for row in day_data]
            return day_data

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return []


if __name__ == "__main__":
    while True:
        print("\nSelect an option:")
        print("=================")
        print("0. Exit")
        print("1. Get all tables")
        print("2. Get overall table data")
        print("3. Get table data by name")
        print("4. Get schedule for a day and group")

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
        else:
            print("Invalid option.")