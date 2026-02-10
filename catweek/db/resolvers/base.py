from sqlalchemy import select

class ResolveError(ValueError):
    pass


def resolve_execute_scalar(conn, stmt, *, label: str):
    try:
        return conn.execute(stmt).scalar_one()
    except Exception:
        raise ResolveError(f"Could not resolve {label}")


def resolve_id(conn, table, id_column, *, where: dict, label: str):
    stmt = select(id_column)
    for col, value in where.items():
        stmt = stmt.where(getattr(table.c, col) == value)

    return resolve_execute_scalar(conn, stmt, label=label)

def is_latin(text: str) -> bool:
    return all("a" <= c.lower() <= "z" for c in text)
