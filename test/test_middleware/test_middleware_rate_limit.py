"""Middleware dispatch: rate-limit exceeded."""

from unittest.mock import patch

_PATCH_IS_BANNED = "core.middleware.firewall.middleware.is_banned"
_PATCH_IS_RATE = "core.middleware.firewall.middleware.is_rate_exceeded"
_PATCH_RECORD = "core.middleware.firewall.middleware.record_illegal_request"
_PATCH_INCR = "core.middleware.firewall.middleware.increment_violation"
_PATCH_BAN = "core.middleware.firewall.middleware.ban_ip"
_PATCH_RESOLVE = "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user"


def test_rate_limit_returns_403(firewall_client):
    with (
        patch(_PATCH_IS_BANNED, return_value=False),
        patch(_PATCH_IS_RATE, return_value=True),
        patch(_PATCH_RECORD),
        patch(_PATCH_INCR, return_value=1),
        patch(_PATCH_BAN),
        patch(_PATCH_RESOLVE, return_value="unknown"),
    ):
        resp = firewall_client.get("/ping")
    assert resp.status_code == 403
    assert "频繁" in resp.json()["detail"]
