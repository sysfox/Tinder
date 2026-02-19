"""ORM 模型：favourites 表。"""

from datetime import datetime

from sqlalchemy import Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from core.database.orm.base import Base

__all__ = ["Favourite"]


class Favourite(Base):
    """favourites 表的 ORM 模型。"""

    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    user_uuid: Mapped[str] = mapped_column(Text, nullable=False)
    types: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
