"""Tests for custom_log output formatting (timestamp, case-insensitivity, empty message)."""

import re
from io import StringIO
from unittest.mock import patch

from core.helper.ContainerCustomLog.index import custom_log


def _capture(level: str, message: str) -> str:
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        custom_log(level, message)
        output = mock_stdout.getvalue()
    return re.sub(r"\033\[[0-9;]*m", "", output)


def test_case_insensitive_level():
    """级别名称不区分大小写（success → SUCCESS）"""
    output = _capture("success", "lower case")
    assert "[SUCCESS]" in output


def test_timestamp_present():
    """输出中包含 YYYY-MM-DD HH:MM:SS 格式时间戳"""
    output = _capture("SUCCESS", "ts test")
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", output)


def test_empty_message():
    """消息为空时仍输出正确的级别标签"""
    output = _capture("SUCCESS", "")
    assert "[SUCCESS]" in output
