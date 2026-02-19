from typing import Any

import psycopg2.extras

from core.database.dao.base import BaseDAO
from core.database.connection.pgsql import pgsql


class IllegalRequestsDAO(BaseDAO):
    """illegal_requests 表的数据访问对象。"""

    TABLE = "illegal_requests"

    def find_by_ip(self, ip: str, limit: int = 100) -> list[dict[str, Any]]:
        """查询指定 IP 的所有违规记录。"""
        conn = pgsql.get_connection()
        if conn is None:
            return []
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE ip = %s ORDER BY happened_at DESC LIMIT %s",
                (ip, limit),
            )
            return [dict(r) for r in cur.fetchall()]

    def find_by_user(self, user: str, limit: int = 100) -> list[dict[str, Any]]:
        """查询指定用户的所有违规记录。"""
        conn = pgsql.get_connection()
        if conn is None:
            return []
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f'SELECT * FROM {self.TABLE} WHERE "user" = %s ORDER BY happened_at DESC LIMIT %s',
                (user, limit),
            )
            return [dict(r) for r in cur.fetchall()]
