import re
import uuid as uuid_lib
from datetime import datetime
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from core.database.connection.redis import redis_conn
from core.helper.ContainerCustomLog.index import custom_log

# ---------------------------------------------------------------------------
# 配置常量
# ---------------------------------------------------------------------------

# 每秒最大请求次数（超过则视为高频攻击）
_MAX_REQUESTS_PER_SECOND = 20

# IP 违规次数上限（达到后封禁）
_BAN_THRESHOLD = 10

# IP 封禁时长（秒）：24 小时
_BAN_DURATION = 86400

# Redis key 前缀
_KEY_RATE = "fw:rate:"       # 速率计数  fw:rate:<ip> -> count (TTL 1s)
_KEY_VIOL = "fw:viol:"       # 违规计数  fw:viol:<ip> -> count (TTL 24h)
_KEY_BAN = "fw:ban:"         # 封禁标记  fw:ban:<ip>  -> "1"  (TTL 24h)

# ---------------------------------------------------------------------------
# 常见爬虫 User-Agent 关键词（不区分大小写）
# ---------------------------------------------------------------------------
_CRAWLER_UA_PATTERNS = re.compile(
    r"(bot|crawler|spider|scraper|curl|wget|python-requests|go-http-client"
    r"|java/|httpclient|axios|node-fetch|libwww|mechanize|scrapy|okhttp"
    r"|headlesschrome|phantomjs|selenium|puppeteer|playwright)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# XSS 检测模式
# ---------------------------------------------------------------------------
_XSS_PATTERNS = re.compile(
    r"(<\s*script[\s\S]*?>|<\s*/\s*script\s*>|javascript\s*:|vbscript\s*:"
    r"|on\w+\s*=\s*[\"']|<\s*iframe|<\s*object|<\s*embed|<\s*link"
    r"|<\s*img[^>]+onerror|document\s*\.\s*cookie|eval\s*\(|expression\s*\()",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# SQL 注入检测模式
# ---------------------------------------------------------------------------
_SQLI_PATTERNS = re.compile(
    r"(\b(select|insert|update|delete|drop|truncate|alter|create|replace"
    r"|union|exec|execute|xp_|sp_)\b.*\b(from|into|table|where|set)\b"
    r"|'[\s\S]*?--"
    r"|;\s*(drop|delete|update|insert|select)"
    r"|\bor\b\s+[\w'\"]+\s*=\s*[\w'\"]+"
    r"|\band\b\s+[\w'\"]+\s*=\s*[\w'\"]+"
    r"|\/\*[\s\S]*?\*\/)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _get_client_ip(request: Request) -> str:
    """从请求中提取客户端真实 IP（兼容反向代理）。"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    if request.client:
        return request.client.host
    return "unknown"


def _resolve_user_from_token(token: str) -> str:
    """通过 token 查询其所有者 uuid，失败时返回 'unknown'。"""
    try:
        from sqlalchemy import func, or_, select

        from core.database.orm.models.tokens import Token
        from core.database.orm.session import get_session

        with get_session() as session:
            stmt = select(Token.belong_to).where(
                Token.uuid == token,
                or_(Token.expired_at.is_(None), Token.expired_at > func.now()),
                Token.current_status != "revoked",
            )
            result = session.scalars(stmt).first()
            return result if result else "unknown"
    except Exception:
        return "unknown"


def _extract_token(request: Request) -> str | None:
    """从请求头 Authorization 或查询参数 token 中提取 token。"""
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip() or None
    return request.query_params.get("token") or None


def _record_illegal_request(
    user: str,
    attack_type: str,
    path: str,
    ip: str,
    ua: str,
) -> None:
    """将违规请求写入 illegal_requests 表，失败时仅打印日志不中断流程。"""
    try:
        from core.database.orm.models.illegal_requests import IllegalRequest
        from core.database.orm.session import get_session

        record = IllegalRequest(
            uuid=str(uuid_lib.uuid4()),
            user=user,
            happened_at=datetime.now(),
            type=attack_type,
            path=path,
            ip=ip,
            ua=ua,
        )
        with get_session() as session:
            session.add(record)
    except Exception as exc:
        custom_log("ERROR", f"[Firewall] 写入 illegal_requests 失败: {exc}")


def _increment_violation(ip: str) -> int:
    """在 Redis 中累加 IP 违规计数，返回当前计数值。"""
    try:
        client = redis_conn.get_client()
        if client is None:
            return 0
        key = f"{_KEY_VIOL}{ip}"
        count = client.incr(key)
        # 每次递增时刷新过期时间为 24h，保证封禁窗口滑动
        client.expire(key, _BAN_DURATION)
        return count
    except Exception as exc:
        custom_log("ERROR", f"[Firewall] Redis 违规计数失败: {exc}")
        return 0


def _ban_ip(ip: str) -> None:
    """在 Redis 中标记 IP 为封禁状态，有效期 24 小时。"""
    try:
        client = redis_conn.get_client()
        if client is None:
            return
        client.set(f"{_KEY_BAN}{ip}", "1", ex=_BAN_DURATION)
        custom_log("WARNING", f"[Firewall] IP 已封禁 24h: {ip}")
    except Exception as exc:
        custom_log("ERROR", f"[Firewall] Redis 封禁 IP 失败: {exc}")


def _is_banned(ip: str) -> bool:
    """检查 IP 是否在 Redis 封禁名单中。"""
    try:
        client = redis_conn.get_client()
        if client is None:
            return False
        return bool(client.exists(f"{_KEY_BAN}{ip}"))
    except Exception:
        return False


def _is_rate_exceeded(ip: str) -> bool:
    """检查 IP 是否超过每秒 20 次的请求速率限制。"""
    try:
        client = redis_conn.get_client()
        if client is None:
            return False
        key = f"{_KEY_RATE}{ip}"
        count = client.incr(key)
        if count == 1:
            client.expire(key, 1)  # 1 秒窗口
        return count > _MAX_REQUESTS_PER_SECOND
    except Exception:
        return False


def _build_reject_response(reason: str) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"detail": reason},
    )


# ---------------------------------------------------------------------------
# 防火墙中间件
# ---------------------------------------------------------------------------

class FirewallMiddleware(BaseHTTPMiddleware):
    """应用层防火墙中间件。

    检测顺序：
    1. IP 封禁检查
    2. 高频访问（速率限制）
    3. 常见爬虫 User-Agent
    4. XSS 攻击特征
    5. SQL 注入特征
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ip = _get_client_ip(request)
        ua = request.headers.get("User-Agent", "")
        path = request.url.path
        query = str(request.url.query)

        # ------------------------------------------------------------------ #
        # 1. IP 封禁检查                                                       #
        # ------------------------------------------------------------------ #
        if _is_banned(ip):
            return _build_reject_response("您的 IP 已被封禁，请 24 小时后重试。")

        # ------------------------------------------------------------------ #
        # 2. 速率限制（超高频访问 > 20次/s）                                    #
        # ------------------------------------------------------------------ #
        if _is_rate_exceeded(ip):
            attack_type = "rate_limit"
            user = self._resolve_user(request)
            _record_illegal_request(user, attack_type, path, ip, ua)
            viol_count = _increment_violation(ip)
            if viol_count >= _BAN_THRESHOLD:
                _ban_ip(ip)
            custom_log("WARNING", f"[Firewall] 速率超限 ip={ip} path={path}")
            return _build_reject_response("请求过于频繁，请稍后再试。")

        # ------------------------------------------------------------------ #
        # 3. 爬虫 User-Agent 检测                                               #
        # ------------------------------------------------------------------ #
        if ua and _CRAWLER_UA_PATTERNS.search(ua):
            attack_type = "crawler"
            user = self._resolve_user(request)
            _record_illegal_request(user, attack_type, path, ip, ua)
            viol_count = _increment_violation(ip)
            if viol_count >= _BAN_THRESHOLD:
                _ban_ip(ip)
            custom_log("WARNING", f"[Firewall] 爬虫 UA 检测 ip={ip} ua={ua}")
            return _build_reject_response("禁止爬虫访问。")

        # ------------------------------------------------------------------ #
        # 4 & 5. XSS / SQL 注入检测（检查 URL 路径和查询参数）                  #
        # ------------------------------------------------------------------ #
        combined = path + "?" + query if query else path
        attack_type = self._detect_attack(combined)
        if attack_type is None:
            # 也检查常用请求头中的注入
            referer = request.headers.get("Referer", "")
            attack_type = self._detect_attack(referer)

        if attack_type:
            user = self._resolve_user(request)
            _record_illegal_request(user, attack_type, path, ip, ua)
            viol_count = _increment_violation(ip)
            if viol_count >= _BAN_THRESHOLD:
                _ban_ip(ip)
            custom_log("WARNING", f"[Firewall] {attack_type} 攻击检测 ip={ip} path={path}")
            return _build_reject_response("请求包含非法内容，已被拦截。")

        # ------------------------------------------------------------------ #
        # 正常请求，放行                                                        #
        # ------------------------------------------------------------------ #
        return await call_next(request)

    # ------------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_user(request: Request) -> str:
        """尝试从请求中解析 token 并返回对应用户，失败时返回 'unknown'。"""
        token = _extract_token(request)
        if not token:
            return "unknown"
        return _resolve_user_from_token(token)

    @staticmethod
    def _detect_attack(text: str) -> str | None:
        """检测文本中的 XSS / SQL 注入特征，返回攻击类型字符串或 None。"""
        if not text:
            return None
        if _XSS_PATTERNS.search(text):
            return "xss"
        if _SQLI_PATTERNS.search(text):
            return "sql_injection"
        return None
