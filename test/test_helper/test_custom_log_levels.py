"""Tests for custom_log level labels (SUCCESS / WARNING / ERROR / unknown)."""

import re
from io import StringIO
from unittest.mock import patch

from core.helper.ContainerCustomLog.index import custom_log


def _capture(level: str, message: str) -> str:
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        custom_log(level, message)
        output = mock_stdout.getvalue()
    return re.sub(r"\033\[[0-9;]*m", "", output)


def test_success_label():
    output = _capture("SUCCESS", "all good")
    assert "[SUCCESS]" in output
    assert "all good" in output


def test_warning_label():
    output = _capture("WARNING", "watch out")
    assert "[WARNING]" in output
    assert "watch out" in output


def test_error_label():
    output = _capture("ERROR", "something failed")
    assert "[ERROR]" in output
    assert "something failed" in output


def test_unknown_level_uses_level_as_label():
    output = _capture("DEBUG", "debug info")
    assert "[DEBUG]" in output
    assert "debug info" in output
