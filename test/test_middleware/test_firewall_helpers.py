"""Tests for core/middleware/firewall helpers (no Redis / DB required)."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient

from core.middleware.firewall.helpers import (
    build_reject_response,
    detect_attack,
    extract_token,
    get_client_ip,
)


# ---------------------------------------------------------------------------
# get_client_ip
# ---------------------------------------------------------------------------

class TestGetClientIp:
    def _make_request(self, headers: dict, client_host: str | None = None):
        req = MagicMock()
        req.headers = headers
        req.client = MagicMock()
        req.client.host = client_host
        return req

    def test_x_forwarded_for_single(self):
        req = self._make_request({"X-Forwarded-For": "1.2.3.4"})
        assert get_client_ip(req) == "1.2.3.4"

    def test_x_forwarded_for_multiple_picks_first(self):
        req = self._make_request({"X-Forwarded-For": "1.2.3.4, 5.6.7.8"})
        assert get_client_ip(req) == "1.2.3.4"

    def test_x_real_ip_fallback(self):
        req = self._make_request({"X-Real-IP": "9.10.11.12"})
        assert get_client_ip(req) == "9.10.11.12"

    def test_client_host_fallback(self):
        req = self._make_request({}, client_host="127.0.0.1")
        assert get_client_ip(req) == "127.0.0.1"

    def test_unknown_when_no_client(self):
        req = MagicMock()
        req.headers = {}
        req.client = None
        assert get_client_ip(req) == "unknown"


# ---------------------------------------------------------------------------
# extract_token
# ---------------------------------------------------------------------------

class TestExtractToken:
    def _make_request(self, auth_header: str = "", token_param: str = ""):
        req = MagicMock()
        req.headers = {"Authorization": auth_header} if auth_header else {}
        req.query_params = {"token": token_param} if token_param else {}
        return req

    def test_bearer_token(self):
        req = self._make_request(auth_header="Bearer abc123")
        assert extract_token(req) == "abc123"

    def test_bearer_token_case_insensitive(self):
        req = self._make_request(auth_header="bearer xyz")
        assert extract_token(req) == "xyz"

    def test_query_param_token(self):
        req = self._make_request(token_param="qptoken")
        assert extract_token(req) == "qptoken"

    def test_no_token_returns_none(self):
        req = self._make_request()
        assert extract_token(req) is None

    def test_empty_bearer_returns_none(self):
        req = self._make_request(auth_header="Bearer ")
        assert extract_token(req) is None


# ---------------------------------------------------------------------------
# detect_attack
# ---------------------------------------------------------------------------

class TestDetectAttack:
    def test_xss_script_tag(self):
        assert detect_attack("<script>alert(1)</script>") == "xss"

    def test_xss_javascript_protocol(self):
        assert detect_attack("javascript:alert(1)") == "xss"

    def test_xss_onerror(self):
        assert detect_attack("<img src=x onerror='bad()'>") == "xss"

    def test_sql_injection_union_select(self):
        assert detect_attack("' UNION SELECT * FROM users--") == "sql_injection"

    def test_sql_injection_drop_table(self):
        assert detect_attack("; DROP TABLE users") == "sql_injection"

    def test_clean_text_returns_none(self):
        assert detect_attack("hello world") is None

    def test_empty_string_returns_none(self):
        assert detect_attack("") is None

    def test_none_returns_none(self):
        assert detect_attack(None) is None


# ---------------------------------------------------------------------------
# build_reject_response
# ---------------------------------------------------------------------------

class TestBuildRejectResponse:
    def test_returns_json_response(self):
        resp = build_reject_response("banned")
        assert isinstance(resp, JSONResponse)

    def test_status_code_403(self):
        resp = build_reject_response("banned")
        assert resp.status_code == 403

    def test_body_contains_reason(self):
        import json
        resp = build_reject_response("test reason")
        body = json.loads(resp.body)
        assert body["detail"] == "test reason"
