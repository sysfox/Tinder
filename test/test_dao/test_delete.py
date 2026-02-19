"""Tests for BaseDAO.delete()."""


def test_delete_existing_returns_true(dao):
    """delete()：删除存在的记录返回 True"""
    dao.create({"uuid": "u-1", "name": "Alice"})
    assert dao.delete("u-1") is True


def test_deleted_row_not_found(dao):
    """delete()：删除后 find_by_uuid 返回 None"""
    dao.create({"uuid": "u-1", "name": "Alice"})
    dao.delete("u-1")
    assert dao.find_by_uuid("u-1") is None


def test_delete_nonexistent_returns_false(dao):
    """delete()：uuid 不存在时返回 False"""
    assert dao.delete("no-such") is False
