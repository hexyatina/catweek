from app import create_app
from app.config import load_settings

cfg = load_settings()
app = create_app()

if __name__ == "__main__":
    app.run(host=cfg.HOST, port=cfg.PORT, debug=cfg.debug)
