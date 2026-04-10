from datetime import date, datetime, time, timedelta, timezone
from hmac import compare_digest
from typing import Any

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.supabase_client import fetch_recent_logs


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
LOG_TYPES = [
    "INITIALIZE_SUCCESS",
    "INITIALIZE_FAILURE",
    "STARTED_TRACKING",
    "TRACK_ONCE",
    "STOPPED_TRACKING",
]


def _display_value(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, str) and not value.strip():
        return "-"
    return str(value)


def _format_timestamp(value: Any) -> str:
    text = _display_value(value)
    if text == "-":
        return text

    try:
        normalized = text.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return text

    return parsed.strftime("%Y-%m-%d %H:%M:%S %Z") or parsed.isoformat()


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_users(value: str | None) -> list[str]:
    if not value:
        return []

    parts = value.replace("\n", ",").split(",")
    return [part.strip() for part in parts if part.strip()]


def _is_authenticated(request: Request) -> bool:
    return bool(request.session.get("authenticated"))


def _title_case_type(value: str) -> str:
    return value.replace("_", " ").title()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    if not _is_authenticated(request):
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "error_message": None,
            },
            status_code=401,
        )

    logs: list[dict[str, str]] = []
    error_message: str | None = None
    start_date = request.query_params.get("start_date", "").strip()
    end_date = request.query_params.get("end_date", "").strip()
    users = request.query_params.get("users", "").strip()
    log_type = request.query_params.get("log_type", "").strip()

    try:
        start_value = _parse_date(start_date) if start_date else None
        end_value = _parse_date(end_date) if end_date else None
        user_ids = _parse_users(users)

        if start_value and end_value and start_value > end_value:
            raise ValueError("Start date must be on or before end date.")
        if log_type and log_type not in LOG_TYPES:
            raise ValueError("Invalid event type.")

        start_at = None
        end_before = None
        if start_value:
            start_at = datetime.combine(start_value, time.min, tzinfo=timezone.utc).isoformat()
        if end_value:
            next_day = end_value + timedelta(days=1)
            end_before = datetime.combine(next_day, time.min, tzinfo=timezone.utc).isoformat()

        rows = fetch_recent_logs(
            start_at=start_at,
            end_before=end_before,
            user_ids=user_ids,
            log_type=log_type or None,
        )
        logs = [
            {
                "created_at": _format_timestamp(row.get("created_at")),
                "user_id": _display_value(row.get("user_id")),
                "type": _display_value(row.get("type")),
                "permission": _display_value(row.get("permission")),
                "entitlement": _display_value(row.get("entitlement")),
                "environment": _display_value(row.get("environment")),
                "error": _display_value(row.get("error")),
            }
            for row in rows
        ]
    except ValueError as exc:
        error_message = str(exc)
    except Exception as exc:
        error_message = str(exc)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "logs": logs,
            "error_message": error_message,
            "filters": {
                "start_date": start_date,
                "end_date": end_date,
                "users": users,
                "log_type": log_type,
            },
            "log_type_options": [
                {"value": value, "label": _title_case_type(value)}
                for value in LOG_TYPES
            ],
        },
    )


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, password: str = Form(...)) -> HTMLResponse:
    settings = get_settings()
    if compare_digest(password, settings.app_password):
        request.session["authenticated"] = True
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "request": request,
            "error_message": "Incorrect password.",
        },
        status_code=401,
    )


@router.post("/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
