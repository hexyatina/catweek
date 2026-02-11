from dataclasses import dataclass
from sqlalchemy import Engine, MetaData
from .engine import create_database_engine
from catweek.db.models import metadata_obj

@dataclass
class AppContext:
    verbose: bool
    remote_database: bool
    engine: Engine
    metadata: MetaData

    @classmethod
    def create(cls,
               verbose: bool = False,
               remote_database: bool = False,
               engine = create_database_engine(remote = False)
               ):
        return cls(
            verbose = verbose,
            remote_database = remote_database,
            engine = engine,
            metadata = metadata_obj
        )