from ..extensions import db

class BaseRepository:
    def __init__(self, session=None):
        self.session = session or db.session