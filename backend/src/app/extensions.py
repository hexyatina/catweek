from flasgger import Swagger
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from .swagger_template import swagger_template, swagger_config


class Base(DeclarativeBase):
    metadata = MetaData(schema="schedule")


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
swagger = Swagger(template=swagger_template, config=swagger_config)
cors = CORS()
talisman = Talisman()
