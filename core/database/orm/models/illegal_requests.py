"""ORM 模型：illegal_requests 表。"""

from datetime import datetime

from sqlalchemy import Index, Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["IllegalRequest"]


class IllegalRequest(Base):
    """illegal_requests 表的 ORM 模型。"""

    __tablename__ = "illegal_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    # "user" is a PostgreSQL reserved word; mapped_column("user", ...) handles quoting
    user: Mapped[str] = mapped_column("user", Text, nullable=False, server_default="unknown")
    happened_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    type: Mapped[str] = mapped_column(Text, nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False)
    ip: Mapped[str] = mapped_column(Text, nullable=False)
    ua: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("idx_illegal_requests_ip", "ip"),
        Index("idx_illegal_requests_happened_at", "happened_at"),
    )
