"""Instagram OAuth endpoints (Instagram Login via Meta Graph API v25.0)."""

import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.config import get_settings
from app.constants import TABLES
from app.database.supabase_client import get_supabase_admin
from app.dependencies import get_current_user
from app.services import instagram_oauth

logger = logging.getLogger("agentesocial.auth")

router = APIRouter()


@router.get("/instagram/authorize")
async def instagram_authorize(user: dict = Depends(get_current_user)):
    """Generate Instagram OAuth authorization URL."""
    try:
        url = instagram_oauth.generate_oauth_url(user["id"])
        return {"authorization_url": url}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instagram/callback")
async def instagram_callback(
    code: str = Query(...),
    state: str = Query(...),
):
    """Handle Instagram OAuth callback. Exchanges code for tokens and saves to DB."""
    settings = get_settings()

    # Validate CSRF state
    user_id = instagram_oauth.validate_and_consume_state(state)
    if not user_id:
        logger.warning("Invalid or expired OAuth state: %s", state[:10])
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/settings?instagram=error&reason=invalid_state"
        )

    try:
        # Exchange code for short-lived token
        token_data = instagram_oauth.exchange_code_for_token(code)
        short_lived_token = token_data["access_token"]

        # Exchange for long-lived token (60 days)
        long_lived_data = instagram_oauth.exchange_for_long_lived_token(short_lived_token)
        access_token = long_lived_data["access_token"]
        expires_in = long_lived_data.get("expires_in", 5184000)

        # Fetch user profile
        profile_data = instagram_oauth.get_instagram_user_profile(access_token)
        ig_user_id = str(profile_data.get("user_id", profile_data.get("id", "")))
        username = profile_data.get("username", "")
        followers_count = profile_data.get("followers_count", 0)

        # Save/update profile in DB
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=expires_in)

        supabase = get_supabase_admin()

        # Check for existing Instagram profile for this user
        existing = (
            supabase.table(TABLES["profiles"])
            .select("id")
            .eq("user_id", user_id)
            .eq("platform", "instagram")
            .limit(1)
            .execute()
        )

        profile_payload = {
            "access_token": access_token,
            "platform_user_id": ig_user_id,
            "handle": f"@{username}" if username else "",
            "followers_count": followers_count,
            "token_expires_at": expires_at.isoformat(),
            "is_active": True,
        }

        if existing.data:
            # Update existing profile
            supabase.table(TABLES["profiles"]).update(profile_payload).eq(
                "id", existing.data[0]["id"]
            ).execute()
            logger.info("Updated Instagram profile for user %s (@%s)", user_id, username)
        else:
            # Insert new profile
            profile_payload.update({
                "user_id": user_id,
                "platform": "instagram",
            })
            supabase.table(TABLES["profiles"]).insert(profile_payload).execute()
            logger.info("Created Instagram profile for user %s (@%s)", user_id, username)

        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/settings?instagram=connected"
        )

    except Exception as e:
        logger.error("Instagram OAuth callback failed: %s", e, exc_info=True)
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/settings?instagram=error&reason=token_exchange_failed"
        )


@router.delete("/instagram/disconnect")
async def instagram_disconnect(user: dict = Depends(get_current_user)):
    """Disconnect Instagram account — deactivate profile and clear tokens."""
    supabase = get_supabase_admin()
    result = (
        supabase.table(TABLES["profiles"])
        .update({
            "is_active": False,
            "access_token": None,
            "refresh_token": None,
            "token_expires_at": None,
        })
        .eq("user_id", user["id"])
        .eq("platform", "instagram")
        .execute()
    )
    disconnected = len(result.data) > 0 if result.data else False
    logger.info("Instagram disconnected for user %s (found=%s)", user["id"], disconnected)
    return {"disconnected": disconnected}


@router.get("/instagram/status")
async def instagram_status(user: dict = Depends(get_current_user)):
    """Check Instagram connection status for current user."""
    supabase = get_supabase_admin()
    result = (
        supabase.table(TABLES["profiles"])
        .select("handle,platform_user_id,followers_count,token_expires_at,is_active")
        .eq("user_id", user["id"])
        .eq("platform", "instagram")
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return {"connected": False}

    profile = result.data[0]
    expires_at = profile.get("token_expires_at")
    expires_in_days = None
    if expires_at:
        try:
            exp = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            delta = exp - datetime.now(timezone.utc)
            expires_in_days = max(0, delta.days)
        except (ValueError, TypeError):
            pass

    return {
        "connected": True,
        "username": profile.get("handle", "").lstrip("@"),
        "followers_count": profile.get("followers_count", 0),
        "expires_at": expires_at,
        "expires_in_days": expires_in_days,
    }
