"""ORM Repository：users 表。

提供与现有 :class:`~core.database.dao.users.UsersDAO` 类似的接口，
但基于 SQLAlchemy 2.x ORM，可与旧版 DAO 共存并逐步迁移。

用法示例::

    from core.database.orm.repositories.users import UsersRepository

    repo = UsersRepository()

    # 查询单条
    user = repo.get_by_uuid("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

    # 分页查询
    users = repo.find_all(limit=20, offset=0)

    # 插入
    new_user = repo.create({
        "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "nickname": "张三",
        "user_role": "user",
    })

    # 更新
    updated = repo.update("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", {"nickname": "李四"})

    # 删除
    success = repo.delete("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
"""

from typing import Any

from sqlalchemy import select

from core.database.orm.models.users import User
from core.database.orm.session import get_session

__all__ = ["UsersRepository"]


class UsersRepository:
    """基于 SQLAlchemy ORM 的 users 表 Repository。"""

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def get_by_uuid(self, uuid: str) -> dict[str, Any] | None:
        """根据 uuid 查询单条用户记录，不存在时返回 None。"""
        with get_session() as session:
            stmt = select(User).where(User.uuid == uuid)
            user = session.scalars(stmt).first()
            return self._to_dict(user) if user else None

    def find_all(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        """分页查询所有用户，默认返回前 100 条。"""
        with get_session() as session:
            stmt = select(User).order_by(User.id).limit(limit).offset(offset)
            return [self._to_dict(u) for u in session.scalars(stmt)]

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """插入新用户记录，返回完整行（含数据库生成的字段）。"""
        # 将 "class" 键映射到模型属性 class_
        kwargs = {("class_" if k == "class" else k): v for k, v in data.items()}
        user = User(**kwargs)
        with get_session() as session:
            session.add(user)
            session.flush()
            session.refresh(user)
            return self._to_dict(user)

    def update(self, uuid: str, data: dict[str, Any]) -> dict[str, Any] | None:
        """根据 uuid 更新字段，返回更新后的行，若记录不存在则返回 None。"""
        with get_session() as session:
            stmt = select(User).where(User.uuid == uuid)
            user = session.scalars(stmt).first()
            if user is None:
                return None
            for key, value in data.items():
                attr = "class_" if key == "class" else key
                setattr(user, attr, value)
            session.flush()
            session.refresh(user)
            return self._to_dict(user)

    def delete(self, uuid: str) -> bool:
        """根据 uuid 删除用户记录，成功删除返回 True，记录不存在返回 False。"""
        with get_session() as session:
            stmt = select(User).where(User.uuid == uuid)
            user = session.scalars(stmt).first()
            if user is None:
                return False
            session.delete(user)
            return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_dict(user: User) -> dict[str, Any]:
        """将 ORM 对象转换为字典（与旧版 DAO 返回格式一致）。"""
        return {
            "id": user.id,
            "uuid": user.uuid,
            "avatar_url": user.avatar_url,
            "nickname": user.nickname,
            "real_name": user.real_name,
            "class": user.class_,
            "class_type": user.class_type,
            "joined_at": user.joined_at,
            "current_status": user.current_status,
            "last_login_at": user.last_login_at,
            "last_login_ip": user.last_login_ip,
            "score": user.score,
            "user_role": user.user_role,
            "title": user.title,
            "invited_by": user.invited_by,
            "views": user.views,
            "other_info": user.other_info,
            "is_verified": user.is_verified,
        }
