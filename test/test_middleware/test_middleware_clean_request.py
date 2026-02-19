"""Middleware dispatch: clean requests that should pass through."""

from unittest.mock import patch

_PATCH_IS_BANNED = "core.middleware.firewall.middleware.is_banned"
_PATCH_IS_RATE = "core.middleware.firewall.middleware.is_rate_exceeded"


def test_clean_request_passes(firewall_client):
    """防火墙：正常请求放行，返回 200"""
    with (
        patch(_PATCH_IS_BANNED, return_value=False),
        patch(_PATCH_IS_RATE, return_value=False),
    ):
        resp = firewall_client.get("/ping")
    assert resp.status_code == 200
