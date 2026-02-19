"""ORM Session 管理：提供线程安全的 scoped_session 单例。

典型用法::

    from core.database.orm.session import get_session

    with get_session() as session:
        user = session.get(User, uuid)

在 FastAPI 路由中，也可以将 :func:`get_session` 用作依赖注入::

    def endpoint(session: Session = Depends(get_session)):
        ...
"""

from contextlib import contextmanager

from sqlalchemy.orm import Session

from core.database.orm.base import get_engine, get_session_factory

__all__ = ["get_session"]

# 模块级延迟初始化的工厂，避免在导入时就连接数据库
_session_factory = None


def _get_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = get_session_factory(get_engine())
    return _session_factory


@contextmanager
def get_session() -> Session:
    """上下文管理器，自动提交或回滚，并在退出时关闭 session。

    示例::

        with get_session() as session:
            session.add(some_object)
    """
    factory = _get_factory()
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
