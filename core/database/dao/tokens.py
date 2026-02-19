from typing import Any

from sqlalchemy import func, or_, select

from core.database.dao.base import BaseDAO
from core.database.orm.models.tokens import Token
from core.database.orm.session import get_session


class TokensDAO(BaseDAO):
    """tokens 表的数据访问对象。"""

    MODEL = Token

    def find_by_belong_to(self, belong_to: str) -> list[dict[str, Any]]:
        """查询指定用户的所有 token。"""
        with get_session() as session:
            objs = session.scalars(
                select(Token).where(Token.belong_to == belong_to)
            )
            return [self._to_dict(o) for o in objs]

    def find_active_by_belong_to(self, belong_to: str) -> list[dict[str, Any]]:
        """查询指定用户的所有未过期 token。"""
        with get_session() as session:
            objs = session.scalars(
                select(Token).where(
                    Token.belong_to == belong_to,
                    or_(Token.expired_at.is_(None), Token.expired_at > func.now()),
                    Token.current_status != "revoked",
                )
            )
            return [self._to_dict(o) for o in objs]

