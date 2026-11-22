from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from connect.core.database import Base


class AdminLog(Base):
    __tablename__ = "admin_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    admin_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        Index("ix_admin_logs_target", "target_type", "target_id"),
        CheckConstraint(
            "target_type IN ('user','team','match','social_match','team_member')",
            name="ck_admin_logs_target_type",
        ),
    )
