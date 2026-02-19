"""Unit tests for get_system_info() function."""

from datetime import datetime

from modules.index.index import get_system_info

APP_NAME = "Tinder"


def test_returns_dict():
    """get_system_info()：返回字典类型"""
    assert isinstance(get_system_info(), dict)


def test_has_name_key():
    """get_system_info()：包含应用名称 'Tinder'"""
    assert get_system_info()["name"] == APP_NAME


def test_has_system_time():
    """get_system_info()：system_time 为 datetime 实例"""
    assert isinstance(get_system_info()["system_time"], datetime)


def test_has_system_version():
    """get_system_info()：system_version 为非空字符串"""
    version = get_system_info()["system_version"]
    assert isinstance(version, str) and len(version) > 0
