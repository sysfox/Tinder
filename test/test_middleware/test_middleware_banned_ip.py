"""Middleware dispatch: banned IP detection and auto-ban on threshold."""

from unittest.mock import patch

_PATCH_IS_BANNED = "core.middleware.firewall.middleware.is_banned"
_PATCH_IS_RATE = "core.middleware.firewall.middleware.is_rate_exceeded"
_PATCH_RECORD = "core.middleware.firewall.middleware.record_illegal_request"
_PATCH_INCR = "core.middleware.firewall.middleware.increment_violation"
_PATCH_BAN = "core.middleware.firewall.middleware.ban_ip"
_PATCH_RESOLVE = "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user"


def test_banned_ip_returns_403(firewall_client):
    with patch(_PATCH_IS_BANNED, return_value=True):
        resp = firewall_client.get("/ping")
    assert resp.status_code == 403
    assert "封禁" in resp.json()["detail"]


def test_ip_banned_when_threshold_reached(firewall_client):
    with (
        patch(_PATCH_IS_BANNED, return_value=False),
        patch(_PATCH_IS_RATE, return_value=True),
        patch(_PATCH_RECORD),
        patch(_PATCH_INCR, return_value=10),
        patch(_PATCH_BAN) as mock_ban,
        patch(_PATCH_RESOLVE, return_value="unknown"),
    ):
        firewall_client.get("/ping")
        mock_ban.assert_called_once()
