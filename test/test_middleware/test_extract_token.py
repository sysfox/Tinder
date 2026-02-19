"""Tests for extract_token helper."""

from unittest.mock import MagicMock

from core.middleware.firewall.helpers import extract_token


def _make_request(auth_header: str = "", token_param: str = ""):
    req = MagicMock()
    req.headers = {"Authorization": auth_header} if auth_header else {}
    req.query_params = {"token": token_param} if token_param else {}
    return req


def test_bearer_token():
    req = _make_request(auth_header="Bearer abc123")
    assert extract_token(req) == "abc123"


def test_bearer_token_case_insensitive():
    req = _make_request(auth_header="bearer xyz")
    assert extract_token(req) == "xyz"


def test_query_param_token():
    req = _make_request(token_param="qptoken")
    assert extract_token(req) == "qptoken"


def test_no_token_returns_none():
    req = _make_request()
    assert extract_token(req) is None


def test_empty_bearer_returns_none():
    req = _make_request(auth_header="Bearer ")
    assert extract_token(req) is None
