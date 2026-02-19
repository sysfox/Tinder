"""Tests for BaseDAO.create()."""


def test_create_returns_dict_with_id(dao):
    result = dao.create({"uuid": "u-1", "name": "Alice"})
    assert isinstance(result, dict)
    assert result["uuid"] == "u-1"
    assert result["name"] == "Alice"
    assert result["id"] is not None


def test_create_multiple_rows(dao):
    dao.create({"uuid": "u-1", "name": "Alice"})
    dao.create({"uuid": "u-2", "name": "Bob"})
    rows = dao.find_all()
    assert len(rows) == 2
