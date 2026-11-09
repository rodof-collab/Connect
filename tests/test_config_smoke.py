# tests/test_schema_smoke.py
import connect.models  # noqa: F401  # импорт регистрирует все модели в Base.metadata
from connect.core.database import Base


def test_all_tables_registered():
    assert sorted(Base.metadata.tables) == sorted(
        [
            "users",
            "profiles",
            "teams",
            "team_members",
            "interests",
            "matches",
            "social_likes",
            "social_matches",
            "admin_logs",
        ]
    )
