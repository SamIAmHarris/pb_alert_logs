from __future__ import annotations

import pytest
from firebase_admin import auth

from product_tests.config import get_test_settings
from product_tests.firebase_auth import create_firebase_test_user, delete_firebase_user


def _firebase_configured() -> bool:
    settings = get_test_settings()
    return bool(
        settings.firebase_project_id
        and (settings.firebase_service_account_file or settings.firebase_service_account_json)
    )


@pytest.mark.integration
def test_create_firebase_user_round_trip() -> None:
    if not _firebase_configured():
        pytest.skip("Firebase Admin env vars are not configured.")

    created_user = create_firebase_test_user()

    try:
        fetched_user = auth.get_user(created_user.uid)
        assert fetched_user.uid == created_user.uid
        assert fetched_user.email == created_user.email
        assert fetched_user.email_verified is True
        assert fetched_user.disabled is False
    finally:
        delete_firebase_user(created_user.uid)
