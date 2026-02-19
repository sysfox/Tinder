"""Tests for BaseDAO.update()."""


def test_update_existing(dao):
    """update()：更新存在的记录并返回更新后的值"""
    dao.create({"uuid": "u-1", "name": "Alice"})
    updated = dao.update("u-1", {"name": "Alicia"})
    assert updated is not None
    assert updated["name"] == "Alicia"


def test_update_nonexistent_returns_none(dao):
    """update()：uuid 不存在时返回 None"""
    assert dao.update("no-such", {"name": "X"}) is None


def test_update_reflected_in_find(dao):
    """update()：更新后通过 find_by_uuid 可查到新值"""
    dao.create({"uuid": "u-1", "name": "Alice"})
    dao.update("u-1", {"name": "Updated"})
    result = dao.find_by_uuid("u-1")
    assert result["name"] == "Updated"
