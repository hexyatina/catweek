import logging
import os
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [entrypoint] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger(__name__)


@dataclass
class Config:
    APP_ENV: str = os.environ.get("APP_ENV", "")
    DB_ENV: str = os.environ.get("DB_ENV", "")
    DB_LOCAL: str = os.environ.get("DATABASE_LOCAL", "")
    DB_REMOTE: str = os.environ.get("DATABASE_REMOTE", "")
    DB_REMOTE_DIRECT: str = os.environ.get("DATABASE_REMOTE_DIRECT", "")
    API_KEY: str = os.environ.get("API_KEY", "")
    PORT: str = os.environ.get("PORT", "5000")
    WORKERS: str = os.environ.get("WORKERS", "4")
    FLASK_APP: str = os.environ.get("FLASK_APP", "wsgi:app")

    @property
    def database_url(self):
        return self.DB_REMOTE if self.DB_ENV == "remote" else self.DB_LOCAL

    def validate(self):
        errors: List[str] = []

        if self.APP_ENV not in ("dev", "prod"):
            errors.append(f"Invalid APP_ENV: {self.APP_ENV}")

        if self.DB_ENV not in ("local", "remote"):
            errors.append(f"Invalid DB_ENV: {self.DB_ENV}")

        if self.DB_ENV == "local" and not self.DB_LOCAL:
            errors.append("DATABASE_LOCAL is not set")
        elif self.DB_ENV == "remote":
            for name, val in (
                    ("DATABASE_REMOTE", self.DB_REMOTE),
                    ("DATABASE_REMOTE_DIRECT", self.DB_REMOTE_DIRECT)
            ):
                if not val or "user:pass" in val:
                    errors.append(f"{name} is not set or contains a placeholder")

        if not self.API_KEY or "generate_a_secure" in self.API_KEY or len(self.API_KEY) < 16:
            errors.append("API_KEY is not set or contains a placeholder")

        for name, val in (("PORT", self.PORT), ("WORKERS", self.WORKERS)):
            if not val.isdigit():
                errors.append(f"{name} must be an integer, got '{val}'")

        if errors:
            for err in errors:
                log.error("Config error: %s", err)
            sys.exit(1)

        log.info("Config validated - APP_ENV = %s, DB_ENV = %s",
                 self.APP_ENV, self.DB_ENV)


def wait_for_postgres(db_url) -> None:
    parsed = urlparse(db_url)
    host = parsed.hostname
    port = parsed.port or 5432
    for attempt in range(1, 31):
        try:
            with socket.create_connection((host, port), timeout=2):
                log.info("Connected to PostgreSQL (attempt %d/30)", attempt)
                return
        except OSError:
            log.info("PostgreSQL not ready yet (attempt %d/30). Retrying in 1s...", attempt)
            time.sleep(1)
    log.error("PostgreSQL did not become ready after 30 attempts. Aborting.")
    sys.exit(1)


def run_command(args: List[str], env_vars: Optional[dict] = None) -> None:
    log.info("Executing: %s", " ".join(args))
    result = subprocess.run(args, env={**os.environ, **(env_vars or {})})
    if result.returncode != 0:
        log.error("Command failed with exit code %s", result.returncode)
        sys.exit(result.returncode)


def main() -> None:
    log.info("===STARTING BACKEND===")

    cfg = Config()
    cfg.validate()

    wait_for_postgres(cfg.database_url)

    migration_env = {"DATABASE_URL": cfg.DB_REMOTE_DIRECT if cfg.DB_ENV == "remote" else cfg.DB_LOCAL}

    log.info("Running migrations...")
    run_command(["flask", "--app", cfg.FLASK_APP, "db", "upgrade"], env_vars=migration_env)

    log.info("Checking seeds...")
    run_command(["flask", "--app", cfg.FLASK_APP, "manage", "seed-if-empty"], env_vars=migration_env)

    if cfg.APP_ENV == "prod":
        log.info("Starting Gunicorn on port %s", cfg.PORT)
        os.execvp("gunicorn", [
            "gunicorn",
            "--bind", f"0.0.0.0:{cfg.PORT}",
            "--workers", cfg.WORKERS,
            "--timeout", "120",
            "--access-logfile", "-",
            "--error-logfile", "-",
            cfg.FLASK_APP
        ])
    else:
        log.info("Starting Flask Dev Server on port %s", cfg.PORT)
        os.execvp("flask", [
            "flask",
            "--app", cfg.FLASK_APP,
            "run",
            "--host", "0.0.0.0",
            "--port", cfg.PORT,
            "--debug"
        ])


if __name__ == "__main__":
    main()
