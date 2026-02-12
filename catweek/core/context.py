from dataclasses import dataclass
from sqlalchemy import Engine, MetaData
from .engine import create_database_engine
from catweek.db.models import schedule_metadata, identity_metadata

@dataclass
class AppContext:
    verbose: bool
    remote_database: bool
    engine: Engine
    schedule_metadata: MetaData
    identity_metadata: MetaData

    @classmethod
    def create(cls, verbose: bool = False, remote_database: bool = False):

        engine = create_database_engine(remote=False)

        return cls(
            verbose = verbose,
            remote_database = remote_database,
            engine = engine,
            schedule_metadata = schedule_metadata,
            identity_metadata = identity_metadata
        )