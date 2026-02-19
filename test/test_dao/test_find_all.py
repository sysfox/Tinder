"""Tests for BaseDAO.find_all() including pagination."""


def test_find_all_empty(dao):
    """find_all()：表为空时返回空列表"""
    assert dao.find_all() == []


def test_find_all_pagination_limit(dao):
    """find_all()：limit 参数限制返回条数"""
    for i in range(5):
        dao.create({"uuid": f"u-{i}", "name": f"user{i}"})
    rows = dao.find_all(limit=3)
    assert len(rows) == 3


def test_find_all_pagination_offset(dao):
    """find_all()：offset 参数跳过指定条数"""
    for i in range(5):
        dao.create({"uuid": f"u-{i}", "name": f"user{i}"})
    rows = dao.find_all(limit=10, offset=3)
    assert len(rows) == 2
