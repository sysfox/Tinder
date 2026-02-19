"""Tests for build_reject_response helper."""

import json

from fastapi.responses import JSONResponse

from core.middleware.firewall.helpers import build_reject_response


def test_returns_json_response():
    """拒绝响应：返回 JSONResponse 类型"""
    resp = build_reject_response("banned")
    assert isinstance(resp, JSONResponse)


def test_status_code_403():
    """拒绝响应：HTTP 状态码为 403"""
    resp = build_reject_response("banned")
    assert resp.status_code == 403


def test_body_contains_reason():
    """拒绝响应：body.detail 包含传入的拒绝原因"""
    resp = build_reject_response("test reason")
    body = json.loads(resp.body)
    assert body["detail"] == "test reason"
