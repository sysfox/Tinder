"""ORM 模型：system_reports 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["SystemReport"]


class SystemReport(Base):
    """system_reports 表的 ORM 模型。"""

    __tablename__ = "system_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    content: Mapped[str | None] = mapped_column(Text)
    frequency: Mapped[int | None] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
