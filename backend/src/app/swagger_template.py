swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Schedule API",
        "description":
            """# Flexible API for college and alike schedules.

## Authentication
All endpoints require `X-Api-Key` header when `ENV=prod`. In `ENV=dev` the API is open.

## Lookup endpoints
Lookup endpoints provide reference data for building filters.

**Stable** — IDs are fixed and never change. Safe to cache permanently:
- `/lookup/days` — 1=Понеділок ... 7=Неділя
- `/lookup/slots` — 1-5=normal duration, 6-10=shortened day
- `/lookup/specialties` — fixed specialty codes

**Dynamic** — IDs increment on each data reset. Refresh each session:
- `/lookup/lecturers`
- `/lookup/venues`
- `/lookup/lessons`
- `/lookup/groups`

## Schedule
- `GET /schedule` — returns compact entry
- `GET /schedule?detailed` — returns full entry with all fields
            """,
        "contact": {
            "email": "pinchukkg@gmail.com",
        },
        "version": "1.0.3"
    },
    "basePath": "/",
    "tags": [
        {"name": "Schedule", "description": "Main schedule endpoint. Add `?detailed` for full response."},
        {"name": "Lookup", "description": "Reference data for filter dropdowns."},
        {"name": "System", "description": "Health and connectivity checks."},
    ],
    "securityDefinitions": {
        "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-Api-Key"}
    },
    "security": [{"ApiKeyAuth": []}],
    "definitions": {
        "ScheduleEntry": {
            "type": "object",
            "properties": {
                "day": {"type": "string", "example": "Понеділок"},
                "time_start": {"type": "string", "example": "09:00"},
                "time_end": {"type": "string", "example": "10:20"},
                "lesson": {"type": "string", "example": "Інженерія Програмного Забезпечення"},
                "lecturer": {"type": "string", "example": "Степанюк"},
                "location": {"type": "string", "example": "14", "x-nullable": True},
                "url": {"type": "string", "example": "https://zoom.us/j/123", "x-nullable": True},
                "week": {"type": "integer", "example": 1},
                "group": {"type": "string", "example": "ІПЗ-31"},
            }
        },
        "ScheduleEntryDetailed": {
            "allOf": [
                {"$ref": "#/definitions/ScheduleEntry"},
                {
                    "type": "object",
                    "properties": {
                        "day_en": {"type": "string", "example": "Monday"},
                        "is_short": {"type": "boolean", "example": False,
                                     "description": "True for shortened day slots (6-10), False for normal slots (1-5)"},
                        "lesson_code": {"type": "string", "example": "ІПЗ"},
                        "lecturer_name": {"type": "string", "example": "Андрій"},
                        "lecturer_middle_name": {"type": "string", "example": "Андрійович"},
                        "specialty_name": {"type": "string", "example": "Інженерія Програмного Забезпечення"},
                        "specialty_code": {"type": "string", "example": "ІПЗ"},
                        "course": {"type": "integer", "example": 3},
                        "group_number": {"type": "integer", "example": 1},
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
            "endpoint": "apispec_json",
            "route": "/apispec.json",
        }
    ],
    "swagger_ui": True,
    "auth": {},
    "specs_route": "/apidocs/",
    "static_url_path": "/flasgger_static",
}
