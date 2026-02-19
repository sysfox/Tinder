from typing import Any

import psycopg2.extras

from core.dao.base import BaseDAO
from core.helper.database.connection.pgsql import pgsql


class RelationsDAO(BaseDAO):
    """relations 表的数据访问对象。

    relations 表没有独立的 uuid 主键，额外提供按 id 查询/删除的方法。
    """

    TABLE = "relations"

    def find_by_uuid(self, uuid: str) -> dict[str, Any] | None:
        raise NotImplementedError("relations 表不包含 uuid 字段，请使用 find_by_id")

    def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any] | None:
        raise NotImplementedError("relations 表不包含 uuid 字段，请使用 update_by_id")

    def delete(self, uuid: str) -> bool:
        raise NotImplementedError("relations 表不包含 uuid 字段，请使用 delete_by_id")

    def find_by_id(self, record_id: int) -> dict[str, Any] | None:
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM {self.TABLE} WHERE id = %s", (record_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_by_tags_uuid(self, tags_uuid: str) -> list[dict[str, Any]]:
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE tags_uuid = %s", (tags_uuid,)
            )
            return [dict(r) for r in cur.fetchall()]

    def update_by_id(self, record_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        conn = pgsql.get_connection()
        assignments = ", ".join([f"{k} = %s" for k in data.keys()])
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"UPDATE {self.TABLE} SET {assignments} WHERE id = %s RETURNING *",
                [*data.values(), record_id],
            )
            conn.commit()
            row = cur.fetchone()
            return dict(row) if row else None

    def delete_by_id(self, record_id: int) -> bool:
        conn = pgsql.get_connection()
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.TABLE} WHERE id = %s", (record_id,))
            conn.commit()
            return cur.rowcount > 0
