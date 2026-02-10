from sqlalchemy import select

class ResolveError(ValueError):
    pass

def resolve_id(conn, table, id_column, *, where: dict, label: str):
    stmt = select(id_column).where(
        *(getattr(table.c, col) == val for col, val in where.items())
    )
    try:
        return conn.execute(stmt).scalar_one()
    except Exception:
        raise ResolveError(f"Failed to resolve {label} using criteria: {where}")


def is_latin(text: str) -> bool:
    return all("a" <= c.lower() <= "z" for c in text)


