
# SCHEDULE API

---


## Quick start using docker

>`cd .\backend\`  
>`cp .env.example .env`   
>`docker compose up --build`

Migrations, seed, and schedule import run automatically on first start.
No need to fill out env if using dev

---

## Docs

Open `http://localhost:5000/` — redirects to Swagger UI.

All endpoints require `X-Api-Key` header when `ENV=prod`.  
In `ENV=dev` the API is open — no key needed.

---

## Local without Docker

Fill in '.env' - minimum required values:

### Dev
Fill in '.env':
- 'ENV=dev'
- 'DATABASE_LOCAL' - your postgres connection string
>1. `uv sync` *synchronizes project dependencies*  
>2. `flask manage reset-db` *resets database if one exists and creates schemas*  
>3. `flask manage seed` *inserts initial data*  
>4. `flask manage import-schedule-yaml` *inserts schedules stored in data/schedules dir*  
>5. `flask --app wsgi:app run --debug` *starts server*

### Prod
Fill in '.env':
- 'ENV=prod'
- 'DATABASE_REMOTE' - pooled connection string
- 'DATABASE_REMOTE_DIRECT' - direct connection string (for migration)
- 'API_KEY' - generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
>1. `cd backend`
>2. `uv sync`
>3. `flask db upgrade` (skip these if the db already exists)
>4. `flask manage seed`
>5. `flask manage import-schedule-yaml`
>6. Linux/Mac: `gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app`  
   Windows: `waitress-serve --host 0.0.0.0 --port 5000 wsgi:app`