"""Tests for BaseDAO.delete()."""


def test_delete_existing_returns_true(dao):
    dao.create({"uuid": "u-1", "name": "Alice"})
    assert dao.delete("u-1") is True


def test_deleted_row_not_found(dao):
    dao.create({"uuid": "u-1", "name": "Alice"})
    dao.delete("u-1")
    assert dao.find_by_uuid("u-1") is None


def test_delete_nonexistent_returns_false(dao):
    assert dao.delete("no-such") is False
