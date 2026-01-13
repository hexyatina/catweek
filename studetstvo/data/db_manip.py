from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

REMOTE_DATABASE = False

if REMOTE_DATABASE:
    #for remote database using neon console
    load_dotenv()
    DATABASE = os.getenv('DATABASE_URL')
    if DATABASE and "+psycopg" not in DATABASE:
        DATABASE = DATABASE.replace("postgresql://", "postgresql+psycopg://")
else:
    #for local database
    DATABASE = "postgresql+psycopg://postgres:1845@localhost:5432/postgres"

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

def add_user_column(table_name):
    try:
        engine = create_engine(DATABASE)
        with engine.connect() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN user_id INT"))

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")
        return []


if __name__ == "__main__":
    while True:
        print("\nSelect an option:")
        print("=================")
        print("0. Exit")
        print("1. Get all tables")
        print("2. Get table data by name")
        print("3. Add user column to table")
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
            table = input("Enter table name: ")
            print("\n--- Input Table ---")
            rows = get_table_data(table)
            for row in rows:
                print(row)
            print("--- Input Table ---")

        elif choice == "3":
            table = input("Enter table name: ")
            print("\n--- Add user column ---")

            print("--- Add user column ---")

        else:
            print("\nInvalid option.")