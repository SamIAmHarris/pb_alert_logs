# Alert Log Viewer

A very small FastAPI app that renders the latest rows from the Supabase `alert_logs` table.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your Supabase values.
4. Start the app:
   `uvicorn app.main:app --reload`

## Environment variables

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_LOGS_TABLE` defaults to `alert_logs`
- `DEFAULT_LOG_LIMIT` defaults to `100`

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
