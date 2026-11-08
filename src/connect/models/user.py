from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, CheckConstraint, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connect.core.database import Base

if TYPE_CHECKING:
    from connect.models.profile import Profile
    from connect.models.user import User


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str | None] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'user'")
    )
    is_banned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    profile: Mapped["Profile | None"] = relationship(
        back_populates="user", uselist=False
    )

    __table_args__ = (
        CheckConstraint("role IN ('user','moderator','admin')", name="ck_users_role"),
    )
