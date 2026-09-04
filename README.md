# Alert Log Viewer

A very small FastAPI app that renders the latest rows from the Supabase `alert_logs` table.

## Setup

Project location:
`/Users/samiam/clients/kaleo/pb/test_portal`

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your Supabase values.
4. Start the app:
   `uvicorn app.main:app --reload`
5. Open:
   `http://127.0.0.1:8000`

You can also run it without activating the virtual environment:
`.venv/bin/uvicorn app.main:app --reload`

## Environment variables

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` for direct DB integration tests
- `SUPABASE_LOGS_TABLE` defaults to `alert_logs`
- `DEFAULT_LOG_LIMIT` defaults to `100`
- `APP_PASSWORD` defaults to `arsenal`
- `SESSION_SECRET` should be set to a random secret in production

## Product flow tests

This repo now has a small pure-Python integration test skeleton under `product_tests/` and `tests/`.

1. Install dependencies:
   `pip install -r requirements.txt`
2. Copy `.env.example` to `.env.test` and fill in test credentials.
3. Put the Firebase service-account JSON at `./firebase-service-account.json`, or set `FIREBASE_SERVICE_ACCOUNT_JSON` in `.env.test`.
4. Run the current skeleton test:
   `pytest -q`

The first test creates a Firebase Auth user, reads it back, confirms key values, and deletes the user in cleanup. Real secrets and service-account files are ignored by git.

## Deploying on Render

This app works well as a Render web service.

### Option 1: Use the Render blueprint

If you deploy from this repo with `render.yaml`, Render will prefill the service settings for you.

### Option 2: Create the service manually

Use these settings in Render:

- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Set these environment variables in Render:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_LOGS_TABLE=alert_logs`
- `DEFAULT_LOG_LIMIT=100`
- `APP_PASSWORD=arsenal`
- `SESSION_SECRET=<random-secret>`
