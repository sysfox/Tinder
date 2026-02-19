"""ORM 模型：system_logs 表。"""

from datetime import datetime

from sqlalchemy import Boolean, Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["SystemLog"]


class SystemLog(Base):
    """system_logs 表的 ORM 模型。"""

    __tablename__ = "system_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    log_level: Mapped[str | None] = mapped_column(Text)
    log_type: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    being_flagged: Mapped[bool | None] = mapped_column(Boolean, server_default="false")
    content: Mapped[str | None] = mapped_column(Text)
    system_version: Mapped[str | None] = mapped_column(Text)
