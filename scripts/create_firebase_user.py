from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from product_tests.firebase_auth import create_firebase_test_user, delete_firebase_user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Firebase test user.")
    parser.add_argument("--email", help="Email to create. Defaults to a unique test email.")
    parser.add_argument("--password", help="Password for the test user.")
    parser.add_argument("--display-name", default="Flow Test User")
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Leave the user in Firebase after creation. By default this script cleans up.",
    )
    args = parser.parse_args()

    user = create_firebase_test_user(
        email=args.email,
        password=args.password,
        display_name=args.display_name,
    )
    print(f"created firebase user uid={user.uid} email={user.email}")

    if not args.keep:
        delete_firebase_user(user.uid)
        print(f"deleted firebase user uid={user.uid}")


if __name__ == "__main__":
    main()
