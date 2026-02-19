"""Tests for BaseDAO CRUD operations using an in-memory SQLite database."""

import pytest
from sqlalchemy import Integer, Text, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

import core.database.connection.db as db_module
from core.database.connection.db import Base
from core.database.dao.base import BaseDAO


# ---------------------------------------------------------------------------
# Lightweight ORM model for testing (avoids PostgreSQL-specific column types)
# ---------------------------------------------------------------------------

class Item(Base):
    """Simple ORM model used only by tests."""
    __tablename__ = "test_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(Text)


class ItemDAO(BaseDAO):
    MODEL = Item


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def sqlite_session(monkeypatch):
    """
    Replace the module-level engine and session factory with an in-memory
    SQLite engine so tests run without a real PostgreSQL instance.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBaseDAOCreate:
    def test_create_returns_dict_with_id(self, dao):
        result = dao.create({"uuid": "u-1", "name": "Alice"})
        assert isinstance(result, dict)
        assert result["uuid"] == "u-1"
        assert result["name"] == "Alice"
        assert result["id"] is not None

    def test_create_multiple_rows(self, dao):
        dao.create({"uuid": "u-1", "name": "Alice"})
        dao.create({"uuid": "u-2", "name": "Bob"})
        rows = dao.find_all()
        assert len(rows) == 2


class TestBaseDAOFindByUuid:
    def test_find_existing(self, dao):
        dao.create({"uuid": "u-1", "name": "Alice"})
        result = dao.find_by_uuid("u-1")
        assert result is not None
        assert result["name"] == "Alice"

    def test_find_nonexistent_returns_none(self, dao):
        assert dao.find_by_uuid("no-such-uuid") is None


class TestBaseDAOFindAll:
    def test_find_all_empty(self, dao):
        assert dao.find_all() == []

    def test_find_all_pagination_limit(self, dao):
        for i in range(5):
            dao.create({"uuid": f"u-{i}", "name": f"user{i}"})
        rows = dao.find_all(limit=3)
        assert len(rows) == 3

    def test_find_all_pagination_offset(self, dao):
        for i in range(5):
            dao.create({"uuid": f"u-{i}", "name": f"user{i}"})
        rows = dao.find_all(limit=10, offset=3)
        assert len(rows) == 2


class TestBaseDAOUpdate:
    def test_update_existing(self, dao):
        dao.create({"uuid": "u-1", "name": "Alice"})
        updated = dao.update("u-1", {"name": "Alicia"})
        assert updated is not None
        assert updated["name"] == "Alicia"

    def test_update_nonexistent_returns_none(self, dao):
        assert dao.update("no-such", {"name": "X"}) is None

    def test_update_reflected_in_find(self, dao):
        dao.create({"uuid": "u-1", "name": "Alice"})
        dao.update("u-1", {"name": "Updated"})
        result = dao.find_by_uuid("u-1")
        assert result["name"] == "Updated"


class TestBaseDAODelete:
    def test_delete_existing_returns_true(self, dao):
        dao.create({"uuid": "u-1", "name": "Alice"})
        assert dao.delete("u-1") is True

    def test_deleted_row_not_found(self, dao):
        dao.create({"uuid": "u-1", "name": "Alice"})
        dao.delete("u-1")
        assert dao.find_by_uuid("u-1") is None

    def test_delete_nonexistent_returns_false(self, dao):
        assert dao.delete("no-such") is False


class TestBaseDAOMissingModel:
    def test_missing_model_raises(self):
        class BadDAO(BaseDAO):
            pass

        with pytest.raises(NotImplementedError):
            BadDAO().find_by_uuid("x")
