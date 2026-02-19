"""ORM 模型：request_logs 表。

request_logs 表使用 request_path 作为唯一键（无 uuid 字段）。
"""

from datetime import datetime

from sqlalchemy import Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["RequestLog"]


class RequestLog(Base):
    """request_logs 表的 ORM 模型。"""

    __tablename__ = "request_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_path: Mapped[str] = mapped_column(Text, nullable=False)
    frequency: Mapped[int | None] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )

    __table_args__ = (UniqueConstraint("request_path"),)
