from app import create_app
from app.config import settings
app = create_app()

if __name__ == "__main__":
    if settings.DEBUG:
        app.run(host=settings.HOST, port=settings.PORT, debug=True)
    else:
        from waitress import serve
        serve(app, host=settings.HOST, port=settings.PORT)