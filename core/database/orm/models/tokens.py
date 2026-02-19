"""ORM 模型：tokens 表。

字段定义与 ``core/database/migrations/SQL/initial_tokens.sql`` 保持一致。
"""

from datetime import datetime

from sqlalchemy import Index, Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["Token"]


class Token(Base):
    """tokens 表的 ORM 模型。"""

    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    belong_to: Mapped[str] = mapped_column(Text, nullable=False)
    permission: Mapped[str] = mapped_column(Text, nullable=False)
    assigner: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    expired_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    current_status: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("idx_tokens_belong_to", "belong_to"),
        Index("idx_tokens_expired_at", "expired_at"),
    )
