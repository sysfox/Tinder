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
    assert client.get("/").status_code == 200


def test_response_contains_name():
    assert client.get("/").json()["name"] == APP_NAME


def test_response_contains_system_version():
    body = client.get("/").json()
    assert "system_version" in body
    assert isinstance(body["system_version"], str)


def test_response_contains_system_time():
    assert "system_time" in client.get("/").json()
