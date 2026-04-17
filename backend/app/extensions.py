from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_talisman import Talisman
from flasgger import Swagger
import logging
from .models import Base
from .swagger_template import swagger_template, swagger_config

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
logger = logging.getLogger("catweek")
swagger = Swagger(template=swagger_template, config=swagger_config)
cors = CORS()
talisman = Talisman()
