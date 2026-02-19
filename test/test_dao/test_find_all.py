"""Tests for BaseDAO.find_all() including pagination."""


def test_find_all_empty(dao):
    assert dao.find_all() == []


def test_find_all_pagination_limit(dao):
    for i in range(5):
        dao.create({"uuid": f"u-{i}", "name": f"user{i}"})
    rows = dao.find_all(limit=3)
    assert len(rows) == 3


def test_find_all_pagination_offset(dao):
    for i in range(5):
        dao.create({"uuid": f"u-{i}", "name": f"user{i}"})
    rows = dao.find_all(limit=10, offset=3)
    assert len(rows) == 2
