from typing import Any

from sqlalchemy import select

from core.database.dao.base import BaseDAO
from core.database.orm.models.illegal_requests import IllegalRequest
from core.database.orm.session import get_session


class IllegalRequestsDAO(BaseDAO):
    """illegal_requests 表的数据访问对象。"""

    MODEL = IllegalRequest

    def find_by_ip(self, ip: str, limit: int = 100) -> list[dict[str, Any]]:
        """查询指定 IP 的所有违规记录。"""
        with get_session() as session:
            objs = session.scalars(
                select(IllegalRequest)
                .where(IllegalRequest.ip == ip)
                .order_by(IllegalRequest.happened_at.desc())
                .limit(limit)
            )
            return [self._to_dict(o) for o in objs]

    def find_by_user(self, user: str, limit: int = 100) -> list[dict[str, Any]]:
        """查询指定用户的所有违规记录。"""
        with get_session() as session:
            objs = session.scalars(
                select(IllegalRequest)
                .where(IllegalRequest.user == user)
                .order_by(IllegalRequest.happened_at.desc())
                .limit(limit)
            )
            return [self._to_dict(o) for o in objs]

