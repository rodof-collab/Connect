from sqlalchemy import DateTime

import connect.models  # noqa: F401
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
            "blocked_users",
            "admin_logs",
        ]
    )


def test_timestamps_are_tz_aware():
    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, DateTime):
                assert col.type.timezone is True, (
                    f"{table.name}.{col.name} без таймзоны"
                )
