"""ORM 模型：tasks 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["Task"]


class Task(Base):
    """tasks 表的 ORM 模型。"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    content: Mapped[str | None] = mapped_column(Text)
    parts: Mapped[str | None] = mapped_column(Text)
    assigner: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
