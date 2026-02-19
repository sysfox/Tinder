"""Integration tests for FirewallMiddleware dispatch logic."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.middleware.firewall.middleware import FirewallMiddleware


def _make_app() -> FastAPI:
    """Create a minimal FastAPI app with FirewallMiddleware and a dummy route."""
    app = FastAPI()
    app.add_middleware(FirewallMiddleware)

    @app.get("/ping")
    async def ping():
        return {"ok": True}

    return app


# Patch all Redis-dependent helpers so tests run without a Redis server.
_PATCH_IS_BANNED = "core.middleware.firewall.middleware.is_banned"
_PATCH_IS_RATE = "core.middleware.firewall.middleware.is_rate_exceeded"
_PATCH_RECORD = "core.middleware.firewall.middleware.record_illegal_request"
_PATCH_INCR = "core.middleware.firewall.middleware.increment_violation"
_PATCH_BAN = "core.middleware.firewall.middleware.ban_ip"
_PATCH_RESOLVE = "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user"


class TestFirewallMiddlewareDispatch:
    def setup_method(self):
        self.app = _make_app()
        self.client = TestClient(self.app, raise_server_exceptions=False)

    # ------------------------------------------------------------------
    # Normal request passes through
    # ------------------------------------------------------------------

    def test_clean_request_passes(self):
        with (
            patch(_PATCH_IS_BANNED, return_value=False),
            patch(_PATCH_IS_RATE, return_value=False),
        ):
            resp = self.client.get("/ping")
        assert resp.status_code == 200

    # ------------------------------------------------------------------
    # Banned IP
    # ------------------------------------------------------------------

    def test_banned_ip_returns_403(self):
        with patch(_PATCH_IS_BANNED, return_value=True):
            resp = self.client.get("/ping")
        assert resp.status_code == 403
        assert "封禁" in resp.json()["detail"]

    # ------------------------------------------------------------------
    # Rate limit exceeded
    # ------------------------------------------------------------------

    def test_rate_limit_returns_403(self):
        with (
            patch(_PATCH_IS_BANNED, return_value=False),
            patch(_PATCH_IS_RATE, return_value=True),
            patch(_PATCH_RECORD),
            patch(_PATCH_INCR, return_value=1),
            patch(_PATCH_BAN),
            patch(
                "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user",
                return_value="unknown",
            ),
        ):
            resp = self.client.get("/ping")
        assert resp.status_code == 403
        assert "频繁" in resp.json()["detail"]

    # ------------------------------------------------------------------
    # Crawler user-agent
    # ------------------------------------------------------------------

    def test_crawler_ua_returns_403(self):
        with (
            patch(_PATCH_IS_BANNED, return_value=False),
            patch(_PATCH_IS_RATE, return_value=False),
            patch(_PATCH_RECORD),
            patch(_PATCH_INCR, return_value=1),
            patch(_PATCH_BAN),
            patch(
                "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user",
                return_value="unknown",
            ),
        ):
            resp = self.client.get("/ping", headers={"User-Agent": "Googlebot/2.1"})
        assert resp.status_code == 403
        assert "爬虫" in resp.json()["detail"]

    # ------------------------------------------------------------------
    # XSS in query
    # ------------------------------------------------------------------

    def test_xss_in_referer_returns_403(self):
        # Use the Referer header to carry the XSS payload; the middleware also
        # inspects this header, and header values are not URL-encoded by httpx.
        with (
            patch(_PATCH_IS_BANNED, return_value=False),
            patch(_PATCH_IS_RATE, return_value=False),
            patch(_PATCH_RECORD),
            patch(_PATCH_INCR, return_value=1),
            patch(_PATCH_BAN),
            patch(
                "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user",
                return_value="unknown",
            ),
        ):
            resp = self.client.get(
                "/ping",
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "http://evil.com/<script>alert(1)</script>",
                },
            )
        assert resp.status_code == 403
        assert "非法" in resp.json()["detail"]

    # ------------------------------------------------------------------
    # IP auto-ban after threshold violations
    # ------------------------------------------------------------------

    def test_ip_banned_when_threshold_reached(self):
        with (
            patch(_PATCH_IS_BANNED, return_value=False),
            patch(_PATCH_IS_RATE, return_value=True),
            patch(_PATCH_RECORD),
            patch(_PATCH_INCR, return_value=10),  # exactly BAN_THRESHOLD
            patch(_PATCH_BAN) as mock_ban,
            patch(
                "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user",
                return_value="unknown",
            ),
        ):
            self.client.get("/ping")
            mock_ban.assert_called_once()
