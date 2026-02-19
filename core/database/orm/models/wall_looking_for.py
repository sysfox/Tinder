"""ORM 模型：wall_looking_for 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["WallLookingFor"]


class WallLookingFor(Base):
    """wall_looking_for 表的 ORM 模型。"""

    __tablename__ = "wall_looking_for"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    current_status: Mapped[str | None] = mapped_column(Text)
    real_status: Mapped[str | None] = mapped_column(Text)
    seeker: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    looking_for_type: Mapped[str | None] = mapped_column(Text)
    last_seen_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    helper: Mapped[str | None] = mapped_column(Text)
    clues: Mapped[str | None] = mapped_column(Text)
