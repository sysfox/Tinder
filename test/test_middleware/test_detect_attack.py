"""Tests for detect_attack helper (XSS and SQL injection detection)."""

from core.middleware.firewall.helpers import detect_attack


def test_xss_script_tag():
    assert detect_attack("<script>alert(1)</script>") == "xss"


def test_xss_javascript_protocol():
    assert detect_attack("javascript:alert(1)") == "xss"


def test_xss_onerror_attribute():
    assert detect_attack("<img src=x onerror='bad()'>") == "xss"


def test_sql_injection_union_select():
    assert detect_attack("' UNION SELECT * FROM users--") == "sql_injection"


def test_sql_injection_drop_table():
    assert detect_attack("; DROP TABLE users") == "sql_injection"


def test_clean_text_returns_none():
    assert detect_attack("hello world") is None


def test_empty_string_returns_none():
    assert detect_attack("") is None


def test_none_returns_none():
    assert detect_attack(None) is None
