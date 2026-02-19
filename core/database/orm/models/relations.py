"""ORM 模型：relations 表。

relations 表没有独立的 uuid 字段，使用自增 id 作为主键。
"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["Relation"]


class Relation(Base):
    """relations 表的 ORM 模型。"""

    __tablename__ = "relations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tags_uuid: Mapped[str] = mapped_column(Text, nullable=False)
    related_uuid: Mapped[str] = mapped_column(Text, nullable=False)
    relation_type: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
