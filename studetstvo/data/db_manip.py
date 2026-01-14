from sqlalchemy import create_engine, text




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
"""
def lala():
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT day_name, day_id FROM days WHERE day_id = :day_id"), {"day_id": 2})
            for row in result:
                print(f"day: {row.day_name}, id: {row.day_id}")

    except Exception as e:
        print(f"Error connecting to PostgresSQL: {e}")

lala()
"""
