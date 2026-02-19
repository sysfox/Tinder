"""ORM 模型：vote 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["Vote"]


class Vote(Base):
    """vote 表的 ORM 模型。"""

    __tablename__ = "vote"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    vote_type: Mapped[str | None] = mapped_column(Text)
    voted_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    committed_by: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)
