from sqlalchemy import create_engine, text
from backend.app.core.config import settings

def create_db_engine(remote: bool = False):

    url = settings.DATABASE_REMOTE if remote else settings.DATABASE_LOCAL

    if not url:
        env_var = 'DATABASE_REMOTE' if remote else 'DATABASE_LOCAL'
        raise ValueError(f"{env_var} is not set in .env file")

    db_engine = create_engine(url, pool_pre_ping=True)

    try:
        with db_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise ConnectionError(f"Error connecting to PostgresSQL: {e}")

    return db_engine

engine = create_db_engine(remote=False)
