"""Tests for detect_attack helper (XSS and SQL injection detection)."""

from core.middleware.firewall.helpers import detect_attack


def test_xss_script_tag():
    """XSS：检测到 <script> 标签"""
    assert detect_attack("<script>alert(1)</script>") == "xss"


def test_xss_javascript_protocol():
    """XSS：检测到 javascript: 协议"""
    assert detect_attack("javascript:alert(1)") == "xss"


def test_xss_onerror_attribute():
    """XSS：检测到 onerror 事件属性"""
    assert detect_attack("<img src=x onerror='bad()'>") == "xss"


def test_sql_injection_union_select():
    """SQL 注入：检测到 UNION SELECT 语句"""
    assert detect_attack("' UNION SELECT * FROM users--") == "sql_injection"


def test_sql_injection_drop_table():
    """SQL 注入：检测到 DROP TABLE 语句"""
    assert detect_attack("; DROP TABLE users") == "sql_injection"


def test_clean_text_returns_none():
    """普通文本：无攻击特征，返回 None"""
    assert detect_attack("hello world") is None


def test_empty_string_returns_none():
    """空字符串：无攻击特征，返回 None"""
    assert detect_attack("") is None


def test_none_returns_none():
    """None 输入：直接返回 None"""
    assert detect_attack(None) is None
