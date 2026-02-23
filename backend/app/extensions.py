from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from .models import Base

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
swagger = Swagger()