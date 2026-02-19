"""ORM 基础设施：声明式基类与 Session 工厂。

使用方式::

    from core.database.orm.base import Base, get_engine, get_session_factory

所有 ORM 模型均应继承 :class:`Base`。
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

__all__ = ["Base", "get_engine", "get_session_factory"]


class Base(DeclarativeBase):
    """所有 ORM 模型的声明式基类。"""


def get_engine(dsn: str | None = None):
    """返回 SQLAlchemy Engine。

    优先使用传入的 *dsn*，否则读取环境变量 ``DATABASE_URL``。
    psycopg2 驱动与现有 psycopg2-binary 依赖兼容，无需额外安装。
    """
    url = dsn or os.environ.get("DATABASE_URL")
    if not url:
        raise EnvironmentError("环境变量 DATABASE_URL 未设置")
    # SQLAlchemy 2.x 需要使用 postgresql+psycopg2:// 格式；
    # 若 DATABASE_URL 使用纯 postgresql:// 则自动替换。
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return create_engine(url, pool_pre_ping=True)


def get_session_factory(engine=None):
    """返回绑定到指定 *engine* 的 Session 工厂。

    若不传入 *engine*，则使用 :func:`get_engine` 创建默认引擎。
    """
    if engine is None:
        engine = get_engine()
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
