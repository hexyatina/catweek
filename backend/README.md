
# SCHEDULE API

---


## Setup
### (Skip there steps if using docker)
>**cp .env.example .env** *to copy the env example*

Fill in '.env' - minimum required values:
- 'API_KEY' - generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `DATABASE_LOCAL` — your local postgres connection string

---

## Docker (recommended)

No `.env` needed for local development.
Docker creates all that is needed by itself.

>docker compose up --build

Migrations, seed, and schedule import run automatically on first start.

---

## Local without Docker

### ***use these commands only if setting up local db in dev***  
>
>1. **uv sync** *synchronizes project dependencies*  
>2. **flask manage reset-db** *resets database if one exists and creates schemas*  
>3. **flask manage seed** *inserts initial data*  
>4. **flask manage import-schedule-yaml** *inserts schedules stored in data/schedules dir*  
>5. **flask --app wsgi:app run --debug** *starts server*



---

## Docs

Open `http://localhost:5000/` — redirects to Swagger UI.

All endpoints require `X-Api-Key` header when `ENV=prod`.
In `ENV=dev` the API is open — no key needed.