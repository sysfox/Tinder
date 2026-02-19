"""Middleware dispatch: XSS / injection attack detection."""

from unittest.mock import patch

_PATCH_IS_BANNED = "core.middleware.firewall.middleware.is_banned"
_PATCH_IS_RATE = "core.middleware.firewall.middleware.is_rate_exceeded"
_PATCH_RECORD = "core.middleware.firewall.middleware.record_illegal_request"
_PATCH_INCR = "core.middleware.firewall.middleware.increment_violation"
_PATCH_BAN = "core.middleware.firewall.middleware.ban_ip"
_PATCH_RESOLVE = "core.middleware.firewall.middleware.FirewallMiddleware._resolve_user"


def test_xss_in_referer_returns_403(firewall_client):
    """防火墙：Referer 头中含 XSS 攻击特征时被拒绝，返回 403"""
    # The middleware also inspects the Referer header for injection payloads.
    with (
        patch(_PATCH_IS_BANNED, return_value=False),
        patch(_PATCH_IS_RATE, return_value=False),
        patch(_PATCH_RECORD),
        patch(_PATCH_INCR, return_value=1),
        patch(_PATCH_BAN),
        patch(_PATCH_RESOLVE, return_value="unknown"),
    ):
        resp = firewall_client.get(
            "/ping",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "http://evil.com/<script>alert(1)</script>",
            },
        )
    assert resp.status_code == 403
    assert "非法" in resp.json()["detail"]
