from functools import lru_cache
from typing import Any

from supabase import Client, create_client

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def fetch_recent_logs(limit: int | None = None) -> list[dict[str, Any]]:
    settings = get_settings()
    client = get_supabase_client()
    query_limit = limit or settings.default_log_limit

    response = (
        client.table(settings.supabase_logs_table)
        .select("id, created_at, user_id, type, permission, entitlement, environment, error")
        .order("created_at", desc=True)
        .limit(query_limit)
        .execute()
    )

    return response.data or []
