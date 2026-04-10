from datetime import datetime
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.supabase_client import fetch_recent_logs


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


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


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    logs: list[dict[str, str]] = []
    error_message: str | None = None

    try:
        rows = fetch_recent_logs()
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
    except Exception as exc:
        error_message = str(exc)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "logs": logs,
            "error_message": error_message,
        },
    )
