from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound

def resolve_id(conn, table, id_column, *, where: dict, label: str):
    stmt = select(id_column).where(
        *(getattr(table.c, col) == val for col, val in where.items())
    )
    try:
        return conn.execute(stmt).scalar_one()
    except NoResultFound:
        raise NoResultFound(f"Lookup Failed: {label} not found with criteria {where}")
    except MultipleResultsFound:
        raise MultipleResultsFound(f"Data Integrity Error: Multiple {label} records found for {where}")
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database infrastructure error: {e}")

def is_latin(text: str) -> bool:
    return all("a" <= c.lower() <= "z" for c in text)