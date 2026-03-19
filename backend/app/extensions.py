from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from .models import Base

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Schedule API",
        "description": "Flexible API for college and alike schedules",
        "contact": {
            "telegramHandle": "KergaX",
            "email": "pinchukkg@gmail.com",
        },
        "version": "1.0.2"
    },
    "basePath": "/",
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-Api-Key"
        }
    },
    "security": [{"ApiKeyAuth": []}],
    "definitions": {
        "ScheduleEntry": {
            "type": "object",
            "properties": {
                "day":      {"type": "string", "example": "Понеділок"},
                "time_start": {"type": "string", "example": "09:00"},
                "time_end":   {"type": "string", "example": "10:20"},
                "lesson":   {"type": "string", "example": "Інженерія Програмного Забезпечення"},
                "lecturer": {"type": "string", "example": "Степанюк"},
                "location": {"type": "string", "example": "14", "x-nullable": True},
                "url":      {"type": "string", "example": "https://zoom.us/j/123", "x-nullable": True},
                "week":     {"type": "integer", "example": 1},
                "group":    {"type": "string", "example": "ІПЗ-31"},
            }
        },
        "ScheduleEntryDetailed": {
            "allOf": [
                {"$ref": "#/definitions/ScheduleEntry"},
                {
                    "type": "object",
                    "properties": {
                        "day_en":              {"type": "string", "example": "Monday"},
                        "is_short":            {"type": "boolean", "example": False, "description": "used for time slots to decide whether lessons are regular duration or shortened"},
                        "lesson_code":         {"type": "string", "example": "ІПЗ"},
                        "lecturer_name":       {"type": "string", "example": "Андрій"},
                        "lecturer_middle_name":{"type": "string", "example": "Андрійович"},
                        "specialty_name":      {"type": "string", "example": "Інженерія Програмного Забезпечення"},
                        "specialty_code":      {"type": "string", "example": "ЖК"},
                        "course":              {"type": "integer", "example": 3},
                        "group_number":        {"type": "integer", "example": 1},
                    }
                }
            ]
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
        }
    ],
    "swagger_ui": True,
    "auth": {},
    "specs_route": "/apidocs/",
    "static_url_path": "/flasgger_static",
}

swagger = Swagger(template=swagger_template, config=swagger_config)
