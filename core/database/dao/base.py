from typing import Any

import psycopg2.extras

from core.database.connection.pgsql import pgsql


class BaseDAO:
    """所有 DAO 的基类，提供针对 PostgreSQL 的通用 CRUD 操作。

    子类只需声明 :attr:`TABLE` 属性，即可继承以下方法：

    * :meth:`find_by_uuid` – 根据 uuid 查询单条记录
    * :meth:`find_all`     – 分页查询所有记录
    * :meth:`create`       – 插入新记录
    * :meth:`update`       – 根据 uuid 更新记录
    * :meth:`delete`       – 根据 uuid 删除记录
    """

    TABLE: str = ""

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def find_by_uuid(self, uuid: str) -> dict[str, Any] | None:
        """根据 uuid 查询单条记录，不存在时返回 None。"""
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM {self.TABLE} WHERE uuid = %s", (uuid,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_all(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        """分页查询所有记录，默认返回前 100 条。"""
        conn = pgsql.get_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"SELECT * FROM {self.TABLE} ORDER BY id LIMIT %s OFFSET %s",
                (limit, offset),
            )
            return [dict(r) for r in cur.fetchall()]

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """插入新记录并返回完整行（含数据库生成的字段）。"""
        conn = pgsql.get_connection()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"INSERT INTO {self.TABLE} ({columns}) VALUES ({placeholders}) RETURNING *",
                list(data.values()),
            )
            conn.commit()
            return dict(cur.fetchone())

    def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any] | None:
        """根据 uuid 更新字段，返回更新后的行，若记录不存在则返回 None。"""
        conn = pgsql.get_connection()
        assignments = ", ".join([f"{k} = %s" for k in data.keys()])
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                f"UPDATE {self.TABLE} SET {assignments} WHERE uuid = %s RETURNING *",
                [*data.values(), uuid],
            )
            conn.commit()
            row = cur.fetchone()
            return dict(row) if row else None

    def delete(self, uuid: str) -> bool:
        """根据 uuid 删除记录，成功删除返回 True，记录不存在返回 False。"""
        conn = pgsql.get_connection()
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.TABLE} WHERE uuid = %s", (uuid,))
            conn.commit()
            return cur.rowcount > 0
