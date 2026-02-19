"""HTTP integration tests for the root GET / route."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.index.index import app as index_router

APP_NAME = "Tinder"

app = FastAPI()
app.include_router(index_router)
client = TestClient(app)


def test_status_200():
    """GET /：请求成功，状态码 200"""
    assert client.get("/").status_code == 200


def test_response_contains_name():
    """GET /：响应 JSON 含应用名称 'Tinder'"""
    assert client.get("/").json()["name"] == APP_NAME


def test_response_contains_system_version():
    """GET /：响应 JSON 含 system_version 字符串"""
    body = client.get("/").json()
    assert "system_version" in body
    assert isinstance(body["system_version"], str)


def test_response_contains_system_time():
    """GET /：响应 JSON 含 system_time 字段"""
    assert "system_time" in client.get("/").json()
