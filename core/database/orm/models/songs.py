"""ORM 模型：songs 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["Song"]


class Song(Base):
    """songs 表的 ORM 模型。"""

    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    singer: Mapped[str | None] = mapped_column(Text)
    platform: Mapped[str | None] = mapped_column(Text)
    committed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    status: Mapped[str | None] = mapped_column(Text)
    vote: Mapped[int | None] = mapped_column(Integer, default=0)
    recommend_by: Mapped[str | None] = mapped_column(Text)
    recommend_words: Mapped[str | None] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)
