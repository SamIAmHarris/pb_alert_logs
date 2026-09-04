from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.auth import UserRecord

from product_tests.config import ROOT_DIR, get_test_settings


def initialize_firebase_admin() -> firebase_admin.App:
    settings = get_test_settings()
    settings.require_firebase_admin()

    try:
        return firebase_admin.get_app()
    except ValueError:
        pass

    if settings.firebase_service_account_info:
        credential = credentials.Certificate(settings.firebase_service_account_info)
    else:
        account_path = Path(settings.firebase_service_account_file)
        if not account_path.is_absolute():
            account_path = ROOT_DIR / account_path
        credential = credentials.Certificate(account_path)

    return firebase_admin.initialize_app(
        credential,
        {"projectId": settings.firebase_project_id},
    )


def unique_test_email(prefix: str = "flow-user") -> str:
    settings = get_test_settings()
    local_part = f"{prefix}-{uuid4().hex[:12]}"
    return f"{local_part}@{settings.test_user_email_domain}"


def create_firebase_test_user(
    email: str | None = None,
    password: str | None = None,
    display_name: str = "Flow Test User",
) -> UserRecord:
    initialize_firebase_admin()
    settings = get_test_settings()
    return auth.create_user(
        email=email or unique_test_email(),
        password=password or settings.test_user_password,
        display_name=display_name,
        email_verified=True,
        disabled=False,
    )


def delete_firebase_user(uid: str) -> None:
    initialize_firebase_admin()
    auth.delete_user(uid)
