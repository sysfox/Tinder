"""ORM Session 管理：提供线程安全的 Session 上下文管理器。

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

__all__ = ["get_session", "dispose_engine"]

# 模块级延迟初始化，避免在导入时就连接数据库
_engine = None
_session_factory = None


def _get_engine_instance():
    global _engine
    if _engine is None:
        _engine = get_engine()
    return _engine


def _get_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = get_session_factory(_get_engine_instance())
    return _session_factory


def dispose_engine() -> None:
    """释放引擎，关闭连接池中的所有连接。在应用停止时调用。"""
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _session_factory = None


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
