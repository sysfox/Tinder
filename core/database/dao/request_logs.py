from typing import Any

import psycopg2.extras

from core.database.dao.base import BaseDAO
from core.database.connection.pgsql import pgsql


class RequestLogsDAO(BaseDAO):
    """request_logs 表的数据访问对象。

    request_logs 表使用 request_path 作为唯一键（非 uuid），
    额外提供按 request_path 查询/更新的方法。
    """

    TABLE = "request_logs"

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
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE request_path = %s",
                (request_path,),
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def upsert_by_path(self, request_path: str) -> dict[str, Any]:
        """若记录不存在则插入，存在则将 frequency 加一。"""
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"""
                INSERT INTO {self.TABLE} (request_path, frequency)
                VALUES (%s, 1)
                ON CONFLICT (request_path)
                DO UPDATE SET frequency = {self.TABLE}.frequency + 1
                RETURNING *
                """,
                (request_path,),
            )
            conn.commit()
            return dict(cur.fetchone())

    def delete_by_path(self, request_path: str) -> bool:
        conn = pgsql.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM {self.TABLE} WHERE request_path = %s",
                (request_path,),
            )
            conn.commit()
            return cur.rowcount > 0
