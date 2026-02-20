from sqlalchemy import inspect, schema
from ..extensions import db

def init_schemas(app):

    with app.app_context():
        inspector = inspect(db.engine)
        existing_schema = inspector.get_schema_names()

        with db.engine.connect() as conn:

            required_schemas = ["schedule"]

            for schema_name in required_schemas:
                if schema_name not in existing_schema:
                    conn.execute(schema.CreateSchema(schema_name))
                    conn.commit()

