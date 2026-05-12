import logging
import os
import subprocess
import sys
from typing import List, Optional

from app.config import load_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [entrypoint] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger(__name__)


def run_command(args: List[str], env_vars: Optional[dict] = None) -> None:
    log.info("Executing: %s", " ".join(args))

    result = subprocess.run(
        args,
        env={**os.environ, **(env_vars or {})},
        capture_output=False,
    )

    if result.returncode != 0:
        log.error("Command failed with exit code %s", result.returncode)
        sys.exit(result.returncode)


def main() -> None:
    log.info("===STARTING BACKEND===")

    cfg = load_settings()

    db_url = cfg.get_database_url(direct=True)

    migration_env = {"DATABASE_URL": db_url}

    log.info("Running migrations...")
    run_command(
        ["flask", "--app", "wsgi:app", "db", "upgrade"],
        env_vars=migration_env
    )

    log.info("Checking seeds...")
    run_command([
        "flask", "--app", "wsgi:app", "manage", "seed-if-empty"],
        env_vars=migration_env
    )

    if cfg.APP_ENV == "prod":
        log.info("Starting Gunicorn on port %s", cfg.PORT)

        os.execvp(
            "gunicorn",
            [
                "gunicorn",
                "--bind", f"0.0.0.0:{cfg.PORT}",
                "--workers", str(cfg.WORKERS),
                "--timeout", "120",
                "--access-logfile", "-",
                "--error-logfile", "-",
                "wsgi:app",
            ])
    else:
        log.info("Starting Flask Dev Server on port %s", cfg.PORT)

        os.execvp(
            "flask",
            [
                "flask",
                "--app", "wsgi:app",
                "run",
                "--host", "0.0.0.0",
                "--port", str(cfg.PORT)
            ])


if __name__ == "__main__":
    main()
