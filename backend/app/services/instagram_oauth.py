"""Instagram OAuth via Meta Graph API v25.0 (Instagram Login)."""

import logging
import secrets
import time
from urllib.parse import urlencode

import httpx

from app.config import get_settings

logger = logging.getLogger("agentesocial.instagram_oauth")

# In-memory CSRF state store: {state_token: {"user_id": ..., "created_at": ...}}
_csrf_states: dict[str, dict] = {}
_STATE_TTL_SECONDS = 600  # 10 minutes

INSTAGRAM_AUTH_URL = "https://www.instagram.com/oauth/authorize"
INSTAGRAM_TOKEN_URL = "https://api.instagram.com/oauth/access_token"
GRAPH_URL = "https://graph.instagram.com"

# Scopes required for Instagram Login (business/creator)
OAUTH_SCOPES = "instagram_business_basic,instagram_business_manage_messages,instagram_business_manage_comments,instagram_business_content_publish,instagram_business_manage_insights"


def _cleanup_expired_states() -> None:
    """Remove expired CSRF states."""
    now = time.time()
    expired = [k for k, v in _csrf_states.items() if now - v["created_at"] > _STATE_TTL_SECONDS]
    for k in expired:
        del _csrf_states[k]


def generate_oauth_url(user_id: str) -> str:
    """Generate Instagram OAuth authorization URL with CSRF state."""
    settings = get_settings()
    if not settings.META_APP_ID or not settings.META_REDIRECT_URI:
        raise ValueError("META_APP_ID and META_REDIRECT_URI must be configured")

    _cleanup_expired_states()

    state = secrets.token_urlsafe(32)
    _csrf_states[state] = {"user_id": user_id, "created_at": time.time()}

    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "response_type": "code",
        "scope": OAUTH_SCOPES,
        "state": state,
    }
    return f"{INSTAGRAM_AUTH_URL}?{urlencode(params)}"


def validate_and_consume_state(state: str) -> str | None:
    """Validate CSRF state and return user_id. Consumes the state (single-use)."""
    _cleanup_expired_states()
    entry = _csrf_states.pop(state, None)
    if entry is None:
        return None
    return entry["user_id"]


def exchange_code_for_token(code: str) -> dict:
    """Exchange authorization code for short-lived access token.

    Returns: {"access_token": str, "user_id": int}
    """
    settings = get_settings()
    payload = {
        "client_id": settings.META_APP_ID,
        "client_secret": settings.META_APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": settings.META_REDIRECT_URI,
        "code": code,
    }
    resp = httpx.post(INSTAGRAM_TOKEN_URL, data=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def exchange_for_long_lived_token(short_lived_token: str) -> dict:
    """Exchange short-lived token for long-lived token (60 days).

    Returns: {"access_token": str, "token_type": str, "expires_in": int}
    """
    settings = get_settings()
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": settings.META_APP_SECRET,
        "access_token": short_lived_token,
    }
    resp = httpx.get(f"{GRAPH_URL}/access_token", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def refresh_long_lived_token(token: str) -> dict:
    """Refresh a long-lived token before it expires.

    Returns: {"access_token": str, "token_type": str, "expires_in": int}
    """
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": token,
    }
    resp = httpx.get(f"{GRAPH_URL}/refresh_access_token", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_instagram_user_profile(token: str) -> dict:
    """Fetch Instagram user profile via Graph API v25.0.

    Returns: {"id": str, "username": str, "name": str, "followers_count": int, ...}
    """
    params = {
        "fields": "user_id,username,name,profile_picture_url,followers_count,follows_count,media_count",
        "access_token": token,
    }
    resp = httpx.get(f"{GRAPH_URL}/v25.0/me", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()
