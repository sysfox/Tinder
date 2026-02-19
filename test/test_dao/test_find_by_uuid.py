"""Tests for BaseDAO.find_by_uuid()."""


def test_find_existing(dao):
    """find_by_uuid()：存在的记录返回对应字典"""
    dao.create({"uuid": "u-1", "name": "Alice"})
    result = dao.find_by_uuid("u-1")
    assert result is not None
    assert result["name"] == "Alice"


def test_find_nonexistent_returns_none(dao):
    """find_by_uuid()：不存在的 uuid 返回 None"""
    assert dao.find_by_uuid("no-such-uuid") is None
