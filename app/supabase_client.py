from functools import lru_cache
from typing import Any

from supabase import Client, create_client

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def fetch_recent_logs(
    limit: int | None = None,
    start_at: str | None = None,
    end_before: str | None = None,
    user_ids: list[str] | None = None,
    log_type: str | None = None,
) -> list[dict[str, Any]]:
    settings = get_settings()
    client = get_supabase_client()
    query_limit = limit or settings.default_log_limit

    query = (
        client.table(settings.supabase_logs_table)
        .select("id, created_at, user_id, type, permission, entitlement, environment, error")
        .order("created_at", desc=True)
        .limit(query_limit)
    )

    if start_at:
        query = query.gte("created_at", start_at)
    if end_before:
        query = query.lt("created_at", end_before)
    if user_ids:
        if len(user_ids) == 1:
            query = query.eq("user_id", user_ids[0])
        else:
            query = query.in_("user_id", user_ids)
    if log_type:
        query = query.eq("type", log_type)

    response = query.execute()

    return response.data or []
