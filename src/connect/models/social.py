from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from connect.core.database import Base


class SocialLike(Base):
    __tablename__ = "social_likes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    from_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    to_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("from_user_id", "to_user_id", name="uq_social_likes_pair"),
        CheckConstraint("from_user_id <> to_user_id", name="ck_social_likes_no_self"),
    )


class SocialMatch(Base):
    __tablename__ = "social_matches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user1_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user2_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'active'")
    )
    matched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uq_social_matches_pair"),
        CheckConstraint("user1_id < user2_id", name="ck_social_matches_order"),
    )
