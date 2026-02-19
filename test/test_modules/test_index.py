"""Tests for modules/index/index.py – the root API route."""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from modules.index.index import app as index_router, get_system_info

APP_NAME = "Tinder"

app = FastAPI()
app.include_router(index_router)

client = TestClient(app)


class TestGetSystemInfo:
    def test_returns_dict(self):
        info = get_system_info()
        assert isinstance(info, dict)

    def test_has_name_key(self):
        info = get_system_info()
        assert info["name"] == APP_NAME

    def test_has_system_time(self):
        from datetime import datetime
        info = get_system_info()
        assert isinstance(info["system_time"], datetime)

    def test_has_system_version(self):
        info = get_system_info()
        assert isinstance(info["system_version"], str)
        assert len(info["system_version"]) > 0


class TestRootRoute:
    def test_status_200(self):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_response_contains_name(self):
        resp = client.get("/")
        assert resp.json()["name"] == APP_NAME

    def test_response_contains_system_version(self):
        resp = client.get("/")
        body = resp.json()
        assert "system_version" in body
        assert isinstance(body["system_version"], str)

    def test_response_contains_system_time(self):
        resp = client.get("/")
        body = resp.json()
        assert "system_time" in body
