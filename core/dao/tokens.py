from typing import Any

import psycopg2.extras

from core.dao.base import BaseDAO
from core.helper.database.connection.pgsql import pgsql


class TokensDAO(BaseDAO):
    """tokens 表的数据访问对象。"""

    TABLE = "tokens"

    def find_by_belong_to(self, belong_to: str) -> list[dict[str, Any]]:
        """查询指定用户的所有 token。"""
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE belong_to = %s", (belong_to,)
            )
            return [dict(r) for r in cur.fetchall()]

    def find_active_by_belong_to(self, belong_to: str) -> list[dict[str, Any]]:
        """查询指定用户的所有未过期 token。"""
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"""
                SELECT * FROM {self.TABLE}
                WHERE belong_to = %s
                  AND (expired_at IS NULL OR expired_at > NOW())
                  AND current_status != 'revoked'
                """,
                (belong_to,),
            )
            return [dict(r) for r in cur.fetchall()]
