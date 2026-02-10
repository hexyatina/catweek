from sqlalchemy import insert

def insert_simple(conn, table, rows):
    conn.execute(insert(table), rows)
