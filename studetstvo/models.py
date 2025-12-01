from studetstvo.data.database import create_database
def create_table():
    conn = create_database()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT
        )
    ''')
    conn.commit()
    conn.close()