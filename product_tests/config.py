from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]


def load_test_environment() -> None:
    """Load repo-local env files without requiring secrets to be committed."""
    load_dotenv(ROOT_DIR / ".env")
    load_dotenv(ROOT_DIR / ".env.test", override=True)


@dataclass(frozen=True)
class TestSettings:
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    firebase_project_id: str
    firebase_service_account_file: str
    firebase_service_account_json: str
    test_user_email_domain: str
    test_user_password: str

    @property
    def firebase_service_account_info(self) -> dict[str, Any] | None:
        if not self.firebase_service_account_json:
            return None
        return json.loads(self.firebase_service_account_json)

    def require_firebase_admin(self) -> None:
        missing = []
        if not self.firebase_project_id:
            missing.append("FIREBASE_PROJECT_ID")
        if not self.firebase_service_account_file and not self.firebase_service_account_json:
            missing.append("FIREBASE_SERVICE_ACCOUNT_FILE or FIREBASE_SERVICE_ACCOUNT_JSON")
        if missing:
            raise RuntimeError(f"Missing Firebase test settings: {', '.join(missing)}")

    def require_supabase(self, service_role: bool = False) -> None:
        missing = []
        if not self.supabase_url:
            missing.append("SUPABASE_URL")
        if not self.supabase_anon_key:
            missing.append("SUPABASE_KEY")
        if service_role and not self.supabase_service_role_key:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")
        if missing:
            raise RuntimeError(f"Missing Supabase test settings: {', '.join(missing)}")


@lru_cache
def get_test_settings() -> TestSettings:
    load_test_environment()
    return TestSettings(
        supabase_url=os.getenv("SUPABASE_URL", "").strip(),
        supabase_anon_key=os.getenv("SUPABASE_KEY", "").strip(),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip(),
        firebase_project_id=os.getenv("FIREBASE_PROJECT_ID", "").strip(),
        firebase_service_account_file=os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE", "").strip(),
        firebase_service_account_json=os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip(),
        test_user_email_domain=os.getenv("TEST_USER_EMAIL_DOMAIN", "example.test").strip() or "example.test",
        test_user_password=os.getenv("TEST_USER_PASSWORD", "ChangeMe123!"),
    )
