from src.app import create_app

app = create_app()

if __name__ == "__main__":
    from src.app.config import settings

    app.run(host=settings.HOST, port=settings.PORT, debug=True)
