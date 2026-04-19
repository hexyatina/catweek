import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging(app) -> None:
    root = logging.getLogger()
    if getattr(app, "_logging_configured", False):
        return
    level = logging.DEBUG if app.config["DEBUG"] else logging.INFO

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    for handler in root.handlers[:]:
        root.removeHandler(handler)

    handlers: list[logging.Handler] = []

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    handlers.append(stream_handler)

    if not app.config["DEBUG"]:
        os.makedirs("logs", exist_ok=True)
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10 ** 6, backupCount=5
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)


    root.setLevel(level)
    for handler in root.handlers:
        handler.setLevel(level)
        root.addHandler(handler)

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if app.config["DEBUG"] else logging.WARNING
    )

    app._logging_configured = True