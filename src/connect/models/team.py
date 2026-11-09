from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connect.core.database import Base

if TYPE_CHECKING:
    from connect.models.user import User


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    max_members: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    owner: Mapped["User"] = relationship()
    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'member'")
    )
    joined_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    left_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship()
    team: Mapped["Team"] = relationship(back_populates="members")

    __table_args__ = (
        Index(
            "uq_team_members_one_active",
            "user_id",
            "team_id",
            unique=True,
            postgresql_where=text("left_at IS NULL"),
        ),
        CheckConstraint(
            "role IN ('owner','member','candidate')", name="ck_team_members_role"
        ),
    )
