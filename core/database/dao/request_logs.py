from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from core.database.dao.base import BaseDAO
from core.database.orm.models.request_logs import RequestLog
from core.database.orm.session import get_session


class RequestLogsDAO(BaseDAO):
    """request_logs 表的数据访问对象。

    request_logs 表使用 request_path 作为唯一键（非 uuid），
    额外提供按 request_path 查询/更新的方法。
    """

    MODEL = RequestLog

    def find_by_uuid(self, uuid: str) -> dict[str, Any] | None:
        raise NotImplementedError(
            "request_logs 表不包含 uuid 字段，请使用 find_by_path"
        )

    def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any] | None:
        raise NotImplementedError(
            "request_logs 表不包含 uuid 字段，请使用 upsert_by_path"
        )

    def delete(self, uuid: str) -> bool:
        raise NotImplementedError(
            "request_logs 表不包含 uuid 字段，请使用 delete_by_path"
        )

    def find_by_path(self, request_path: str) -> dict[str, Any] | None:
        with get_session() as session:
            obj = session.scalars(
                select(RequestLog).where(RequestLog.request_path == request_path)
            ).first()
            return self._to_dict(obj) if obj else None

    def upsert_by_path(self, request_path: str) -> dict[str, Any]:
        """若记录不存在则插入，存在则将 frequency 加一。"""
        with get_session() as session:
            stmt = (
                pg_insert(RequestLog)
                .values(request_path=request_path, frequency=1)
                .on_conflict_do_update(
                    index_elements=["request_path"],
                    set_={"frequency": RequestLog.__table__.c.frequency + 1},
                )
            )
            session.execute(stmt)
            session.flush()
            obj = session.scalars(
                select(RequestLog).where(RequestLog.request_path == request_path)
            ).first()
            return self._to_dict(obj)

    def delete_by_path(self, request_path: str) -> bool:
        with get_session() as session:
            obj = session.scalars(
                select(RequestLog).where(RequestLog.request_path == request_path)
            ).first()
            if obj is None:
                return False
            session.delete(obj)
            return True

