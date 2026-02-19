"""Tests for get_client_ip helper."""

from unittest.mock import MagicMock

from core.middleware.firewall.helpers import get_client_ip


def _make_request(headers: dict, client_host: str | None = None):
    req = MagicMock()
    req.headers = headers
    req.client = MagicMock()
    req.client.host = client_host
    return req


def test_x_forwarded_for_single():
    """X-Forwarded-For 单个 IP：直接返回该 IP"""
    req = _make_request({"X-Forwarded-For": "1.2.3.4"})
    assert get_client_ip(req) == "1.2.3.4"


def test_x_forwarded_for_multiple_picks_first():
    """X-Forwarded-For 多个 IP：返回第一个（真实客户端）"""
    req = _make_request({"X-Forwarded-For": "1.2.3.4, 5.6.7.8"})
    assert get_client_ip(req) == "1.2.3.4"


def test_x_real_ip_fallback():
    """无 X-Forwarded-For 时回退到 X-Real-IP"""
    req = _make_request({"X-Real-IP": "9.10.11.12"})
    assert get_client_ip(req) == "9.10.11.12"


def test_client_host_fallback():
    """无代理头时回退到 request.client.host"""
    req = _make_request({}, client_host="127.0.0.1")
    assert get_client_ip(req) == "127.0.0.1"


def test_unknown_when_no_client():
    """无任何来源 IP 信息时返回 'unknown'"""
    req = MagicMock()
    req.headers = {}
    req.client = None
    assert get_client_ip(req) == "unknown"
