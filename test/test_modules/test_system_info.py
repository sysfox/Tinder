"""Unit tests for get_system_info() function."""

from datetime import datetime

from modules.index.index import get_system_info

APP_NAME = "Tinder"


def test_returns_dict():
    assert isinstance(get_system_info(), dict)


def test_has_name_key():
    assert get_system_info()["name"] == APP_NAME


def test_has_system_time():
    assert isinstance(get_system_info()["system_time"], datetime)


def test_has_system_version():
    version = get_system_info()["system_version"]
    assert isinstance(version, str) and len(version) > 0
