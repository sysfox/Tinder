"""Shared ORM model, DAO class, and SQLite fixtures for DAO tests."""

import pytest
from sqlalchemy import Integer, Text, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

import core.database.connection.db as db_module
from core.database.connection.db import Base
from core.database.dao.base import BaseDAO


class Item(Base):
    """Lightweight ORM model for testing (avoids PostgreSQL-specific types)."""
    __tablename__ = "test_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(Text)


class ItemDAO(BaseDAO):
    MODEL = Item


@pytest.fixture(autouse=True)
def sqlite_session(monkeypatch):
    """Swap the global engine/session for an in-memory SQLite instance."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    monkeypatch.setattr(db_module, "_engine", engine)
    monkeypatch.setattr(db_module, "_session_factory", factory)
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def dao() -> ItemDAO:
    return ItemDAO()
