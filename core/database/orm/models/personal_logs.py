"""ORM 模型：personal_logs 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["PersonalLog"]


class PersonalLog(Base):
    """personal_logs 表的 ORM 模型。"""

    __tablename__ = "personal_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    user_uuid: Mapped[str] = mapped_column(Text, nullable=False)
    log_level: Mapped[str | None] = mapped_column(Text)
    log_type: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
