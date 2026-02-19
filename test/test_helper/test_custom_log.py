"""Tests for core/helper/ContainerCustomLog/index.py"""

import re
from io import StringIO
from unittest.mock import patch

import pytest

from core.helper.ContainerCustomLog.index import custom_log


def _capture_log(level: str, message: str) -> str:
    """Run custom_log and return the printed output (ANSI codes stripped)."""
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        custom_log(level, message)
        output = mock_stdout.getvalue()
    # Strip ANSI escape sequences so assertions remain colour-agnostic.
    return re.sub(r"\033\[[0-9;]*m", "", output)


class TestCustomLog:
    def test_success_label(self):
        output = _capture_log("SUCCESS", "all good")
        assert "[SUCCESS]" in output
        assert "all good" in output

    def test_warning_label(self):
        output = _capture_log("WARNING", "watch out")
        assert "[WARNING]" in output
        assert "watch out" in output

    def test_error_label(self):
        output = _capture_log("ERROR", "something failed")
        assert "[ERROR]" in output
        assert "something failed" in output

    def test_unknown_level_uses_level_as_label(self):
        output = _capture_log("DEBUG", "debug info")
        assert "[DEBUG]" in output
        assert "debug info" in output

    def test_case_insensitive_level(self):
        output = _capture_log("success", "lower case")
        assert "[SUCCESS]" in output

    def test_timestamp_present(self):
        output = _capture_log("SUCCESS", "ts test")
        # Timestamp format: YYYY-MM-DD HH:MM:SS
        assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", output)

    def test_empty_message(self):
        output = _capture_log("SUCCESS", "")
        assert "[SUCCESS]" in output
