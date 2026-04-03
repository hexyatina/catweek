import logging
import os
from logging.handlers import RotatingFileHandler
from ..extensions import logger as ext_logger

def configure_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    ext_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

    file_handler = RotatingFileHandler('logs/catweek.log', maxBytes=10 ** 6, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    ext_logger.addHandler(file_handler)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)