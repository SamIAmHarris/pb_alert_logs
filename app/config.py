from functools import lru_cache
import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.supabase_url = os.getenv("SUPABASE_URL", "").strip()
        self.supabase_key = os.getenv("SUPABASE_KEY", "").strip()
        self.supabase_logs_table = os.getenv("SUPABASE_LOGS_TABLE", "alert_logs").strip() or "alert_logs"
        self.default_log_limit = int(os.getenv("DEFAULT_LOG_LIMIT", "100"))

        missing = [
            name
            for name, value in (
                ("SUPABASE_URL", self.supabase_url),
                ("SUPABASE_KEY", self.supabase_key),
            )
            if not value
        ]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Missing required environment variables: {joined}")


@lru_cache
def get_settings() -> Settings:
    return Settings()
