from sqlalchemy import create_engine, text
from .config import DATABASE_LOCAL, DATABASE_REMOTE

def create_database_engine(remote: bool = False):

    url = DATABASE_REMOTE if remote else DATABASE_LOCAL

    if not url:
        env_var = 'DATABASE_REMOTE' if remote else 'DATABASE_LOCAL'
        raise ValueError(f"{env_var} is not set in .env file")

    engine = create_engine(url, pool_pre_ping=True)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise ConnectionError(f"Error connecting to PostgresSQL: {e}")

    return engine