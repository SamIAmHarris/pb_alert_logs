from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from product_tests.config import get_test_settings


@lru_cache
def get_supabase_anon_client() -> Client:
    settings = get_test_settings()
    settings.require_supabase()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@lru_cache
def get_supabase_service_client() -> Client:
    settings = get_test_settings()
    settings.require_supabase(service_role=True)
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
