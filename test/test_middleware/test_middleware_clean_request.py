"""Middleware dispatch: clean requests that should pass through."""

from unittest.mock import patch

_PATCH_IS_BANNED = "core.middleware.firewall.middleware.is_banned"
_PATCH_IS_RATE = "core.middleware.firewall.middleware.is_rate_exceeded"


def test_clean_request_passes(firewall_client):
    with (
        patch(_PATCH_IS_BANNED, return_value=False),
        patch(_PATCH_IS_RATE, return_value=False),
    ):
        resp = firewall_client.get("/ping")
    assert resp.status_code == 200
