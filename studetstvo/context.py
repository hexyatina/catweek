from dataclasses import dataclass
from sqlalchemy import Engine, MetaData

@dataclass
class AppContext:
    verbose: bool
    remote_database: bool
    engine: Engine
    metadata: MetaData
