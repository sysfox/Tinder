"""Tests for BaseDAO MODEL guard (missing MODEL attribute raises NotImplementedError)."""

import pytest

from core.database.dao.base import BaseDAO


def test_missing_model_raises():
    """未设置 MODEL 属性的 DAO 抛出 NotImplementedError"""
    class BadDAO(BaseDAO):
        pass

    with pytest.raises(NotImplementedError):
        BadDAO().find_by_uuid("x")
