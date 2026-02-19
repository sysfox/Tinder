"""Shared fixtures for FirewallMiddleware integration tests."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.middleware.firewall.middleware import FirewallMiddleware


@pytest.fixture()
def firewall_client():
    """Return a TestClient wrapping a minimal app with FirewallMiddleware."""
    app = FastAPI()
    app.add_middleware(FirewallMiddleware)

    @app.get("/ping")
    async def ping():
        return {"ok": True}

    return TestClient(app, raise_server_exceptions=False)
