"""Centralized Instagram credential resolution per user.

Resolution order: DB per-user token -> env var fallback -> None
"""

import logging
from datetime import datetime, timedelta, timezone

from app.config import get_settings
from app.constants import TABLES
from app.database.supabase_client import get_supabase_admin

logger = logging.getLogger("agentesocial.token_manager")


def get_user_instagram_credentials(user_id: str = "") -> tuple[str, str] | None:
    """Resolve Instagram credentials for a user.

    Returns (access_token, account_id) or None.
    Priority: DB per-user -> env var fallback.
    """
    if user_id:
        creds = _get_credentials_from_db(user_id)
        if creds:
            return creds

    return _get_fallback_credentials()


def _get_credentials_from_db(user_id: str) -> tuple[str, str] | None:
    """Fetch active Instagram profile from DB and refresh token if needed."""
    try:
        supabase = get_supabase_admin()
        result = (
            supabase.table(TABLES["profiles"])
            .select("id,access_token,platform_user_id,token_expires_at")
            .eq("user_id", user_id)
            .eq("platform", "instagram")
            .eq("is_active", True)
            .limit(1)
            .execute()
        )

        if not result.data:
            return None

        profile = result.data[0]
        access_token = profile.get("access_token")
        platform_user_id = profile.get("platform_user_id", "me")

        if not access_token:
            return None

        # Refresh token if expiring within 7 days
        expires_at = profile.get("token_expires_at")
        if expires_at:
            _maybe_refresh_token(profile["id"], access_token, expires_at)
            # Re-read in case token was refreshed
            refreshed = (
                supabase.table(TABLES["profiles"])
                .select("access_token")
                .eq("id", profile["id"])
                .limit(1)
                .execute()
            )
            if refreshed.data:
                access_token = refreshed.data[0]["access_token"]

        return access_token, platform_user_id

    except Exception as e:
        logger.warning("Failed to get credentials from DB for user %s: %s", user_id, e)
        return None


def _maybe_refresh_token(profile_id: str, token: str, expires_at: str) -> None:
    """Refresh the long-lived token if it expires within 7 days."""
    try:
        exp = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        if exp - now > timedelta(days=7):
            return  # Still fresh

        from app.services.instagram_oauth import refresh_long_lived_token

        result = refresh_long_lived_token(token)
        new_token = result["access_token"]
        expires_in = result.get("expires_in", 5184000)  # default 60 days
        new_expires = now + timedelta(seconds=expires_in)

        supabase = get_supabase_admin()
        supabase.table(TABLES["profiles"]).update({
            "access_token": new_token,
            "token_expires_at": new_expires.isoformat(),
        }).eq("id", profile_id).execute()

        logger.info("Token refreshed for profile %s, new expiry: %s", profile_id, new_expires)

    except Exception as e:
        logger.error("Failed to refresh token for profile %s: %s", profile_id, e)


def _get_fallback_credentials() -> tuple[str, str] | None:
    """Fallback to env var credentials for backward compatibility."""
    settings = get_settings()
    token = settings.INSTAGRAM_ACCESS_TOKEN
    account_id = settings.INSTAGRAM_BUSINESS_ACCOUNT_ID
    if not token or not account_id:
        return None
    return token, account_id
