import logging
import os
import shutil
import socket
import subprocess
import sys
import time
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [entrypoint] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

log = logging.getLogger(__name__)

APP_ENV = os.environ.get("APP_ENV", "")
DB_ENV = os.environ.get("DB_ENV", "")
DB_LOCAL = os.environ.get("DATABASE_LOCAL", "")
DB_REMOTE = os.environ.get("DATABASE_REMOTE", "")
DB_REMOTE_DIRECT = os.environ.get("DATABASE_REMOTE_DIRECT", "")
API_KEY = os.environ.get("API_KEY", "")
PORT = os.environ.get("PORT", "5000")
WORKERS = os.environ.get("WORKERS", "4")
FLASK_APP = os.environ.get("FLASK_APP", "wsgi:app")

def validate_env() -> None:
    errors = []

    if APP_ENV not in ("dev", "prod"):
        errors.append("APP_ENV must be 'dev' or 'prod'")

    if DB_ENV not in ("local", "remote"):
        errors.append("DB_ENV must be 'local' or 'remote'")

    if DB_ENV == "local":
        if not DB_LOCAL:
            errors.append("DATABASE_LOCAL is not set")
    else:
        for name, val in (
                ("DATABASE_REMOTE", DB_REMOTE),
                ("DATABASE_REMOTE_DIRECT", DB_REMOTE_DIRECT)
        ):
            if not val or "user:pass" in val:
                errors.append(f"{name} is not set or contains a placeholder")

    if not API_KEY or "generate_a_secure" in API_KEY:
        errors.append("API_KEY is not set or contains a placeholder")

    for name, val in (("PORT", PORT), ("WORKERS", WORKERS)):
        if not val.isdigit():
            errors.append(f"{name} must be an integer, got '{val}'")

    if errors:
        for err in errors:
            log.error("Config error: %s", err)
        sys.exit(1)

    log.info("Config validated - APP_ENV = %s, DB_ENV = %s",
             APP_ENV, DB_ENV)


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


def run_flask_command(*args: str) -> None:
    cmd = ["flask", "--app", FLASK_APP, *args]
    log.info("Running: %s", " ".join(cmd))

    result = subprocess.run(cmd)

    if result.returncode != 0:
        log.error("Command failed with exit code %s", result.returncode)
        sys.exit(result.returncode)


def start_server() -> None:
    if APP_ENV == "prod":
        gunicorn = shutil.which("gunicorn")
        if not gunicorn:
            log.error("gunicorn not found in PATH. Aborting.")
            sys.exit(1)
        log.info("Starting gunicorn prod server (workers=%s, port=%s)", WORKERS, PORT)
        os.execv(gunicorn, [
            "gunicorn",
            "--bind", f"0.0.0.0:{PORT}",
            "--workers", WORKERS,
            "--timeout", "120",
            "--access-logfile", "-",
            "--error-logfile", "-",
            FLASK_APP,
        ])
    else:
        flask = shutil.which("flask")
        if not flask:
            log.error("flask not found in PATH. Aborting.")
            sys.exit(1)
        log.info("Starting Flask dev server (port=%s)", PORT)
        log.info("API key auth disabled in dev mode")
        os.execv(flask, [
            "flask", "--app", FLASK_APP,
            "run", "--host", "0.0.0.0", "--port", PORT, "--debug"
        ])


def main() -> None:
    log.info("===STARTING BACKEND===")

    validate_env()

    db_url = DB_LOCAL if DB_ENV == "local" else DB_REMOTE
    wait_for_postgres(db_url)

    run_flask_command("db", "upgrade")
    run_flask_command("manage", "seed-if-empty")

    start_server()


if __name__ == "__main__":
    main()
