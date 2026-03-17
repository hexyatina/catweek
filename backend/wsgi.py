from app import create_app
from app.config import settings
app = create_app()

if settings.DEBUG:
    if __name__ == "__main__":
        app.run()