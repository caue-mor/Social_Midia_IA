from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.schemas import SocialProfileCreate
from app.constants import TABLES

router = APIRouter()


@router.post("/profiles")
async def add_social_profile(
    request: SocialProfileCreate,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    data = {
        "user_id": user["id"],
        "platform": request.platform,
        "handle": request.handle,
        "access_token": request.access_token,
        "platform_user_id": request.platform_user_id,
    }
    result = supabase.table(TABLES["profiles"]).insert(data).execute()
    return {"profile": result.data[0] if result.data else None}


@router.get("/profiles")
async def list_social_profiles(
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    result = supabase.table(TABLES["profiles"]).select("*").eq("user_id", user["id"]).execute()
    return {"profiles": result.data}


@router.delete("/profiles/{profile_id}")
async def remove_social_profile(
    profile_id: str,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    supabase.table(TABLES["profiles"]).delete().eq("id", profile_id).eq("user_id", user["id"]).execute()
    return {"deleted": True}


# Brand Voice
@router.post("/brand-voice")
async def save_brand_voice(
    request: dict,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    data = {
        "user_id": user["id"],
        "name": request.get("name", "Default"),
        "tone": request.get("tone", ""),
        "vocabulary": request.get("vocabulary", []),
        "avoid_words": request.get("avoid_words", []),
        "target_audience": request.get("target_audience", ""),
        "is_active": True,
    }
    # Deactivate existing
    supabase.table(TABLES["brand_voice_profiles"]).update({"is_active": False}).eq("user_id", user["id"]).execute()
    result = supabase.table(TABLES["brand_voice_profiles"]).insert(data).execute()
    return {"brand_voice": result.data[0] if result.data else None}


@router.get("/brand-voice")
async def get_brand_voice(
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    result = supabase.table(TABLES["brand_voice_profiles"]).select("*").eq("user_id", user["id"]).eq("is_active", True).limit(1).execute()
    return {"brand_voice": result.data[0] if result.data else None}
