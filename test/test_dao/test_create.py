"""Tests for BaseDAO.create()."""


def test_create_returns_dict_with_id(dao):
    """create()：插入新记录并返回含 id 的字典"""
    result = dao.create({"uuid": "u-1", "name": "Alice"})
    assert isinstance(result, dict)
    assert result["uuid"] == "u-1"
    assert result["name"] == "Alice"
    assert result["id"] is not None


def test_create_multiple_rows(dao):
    """create()：连续插入多条记录均可查到"""
    dao.create({"uuid": "u-1", "name": "Alice"})
    dao.create({"uuid": "u-2", "name": "Bob"})
    rows = dao.find_all()
    assert len(rows) == 2
