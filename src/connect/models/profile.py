from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connect.core.database import Base

if TYPE_CHECKING:
    from connect.models.profile import Profile
    from connect.models.user import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    bio: Mapped[str | None] = mapped_column(Text)
    game: Mapped[str | None] = mapped_column(String(64))
    skill_level: Mapped[str | None] = mapped_column(String(20))
    privacy: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'public'")
    )
    contact: Mapped[str | None] = mapped_column(String(128))
    data_consent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    __table_args__ = (
        CheckConstraint(
            "skill_level IN ('beginner','middle','advanced','pro')",
            name="ck_profiles_skill",
        ),
        CheckConstraint(
            "privacy IN ('public','friends_only','private')", name="ck_profiles_privacy"
        ),
    )
