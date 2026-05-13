import logging
import os

from app.config import load_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [entrypoint] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger(__name__)


def main() -> None:
    log.info("===STARTING BACKEND===")

    cfg = load_settings()

    if cfg.APP_ENV == "prod":
        log.info("Starting Gunicorn on port %s", cfg.PORT)

        os.execvp(
            "gunicorn",
            [
                "gunicorn",
                "--bind",
                f"0.0.0.0:{cfg.PORT}",
                "--workers",
                str(cfg.WORKERS),
                "--timeout",
                "120",
                "--access-logfile",
                "-",
                "--error-logfile",
                "-",
                "wsgi:app",
            ],
        )
    else:
        log.info("Starting Flask Dev Server on port %s", cfg.PORT)

        os.execvp(
            "flask",
            [
                "flask",
                "--app",
                "wsgi:app",
                "run",
                "--host",
                "0.0.0.0",
                "--port",
                str(cfg.PORT),
            ],
        )


if __name__ == "__main__":
    main()
