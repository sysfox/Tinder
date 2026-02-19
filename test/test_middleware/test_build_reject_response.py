"""Tests for build_reject_response helper."""

import json

from fastapi.responses import JSONResponse

from core.middleware.firewall.helpers import build_reject_response


def test_returns_json_response():
    resp = build_reject_response("banned")
    assert isinstance(resp, JSONResponse)


def test_status_code_403():
    resp = build_reject_response("banned")
    assert resp.status_code == 403


def test_body_contains_reason():
    resp = build_reject_response("test reason")
    body = json.loads(resp.body)
    assert body["detail"] == "test reason"
