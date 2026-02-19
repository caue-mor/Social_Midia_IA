import logging
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.constants import TABLES

router = APIRouter()
logger = logging.getLogger("agentesocial.insights")


@router.get("/dashboard")
async def insights_dashboard(
    user: dict = Depends(get_current_user),
    platform: str = None,
):
    """Retorna dashboard de insights: patterns, growth, recommendations."""
    from app.services.learning_service import analyze_content_patterns

    try:
        data = await analyze_content_patterns(user["id"], platform)
        return data
    except Exception as e:
        logger.error(f"Error generating insights dashboard: {e}")
        return {"patterns": {}, "growth": {}, "recommendations": []}


@router.get("/top-content")
async def top_content(
    user: dict = Depends(get_current_user),
    platform: str = None,
    limit: int = 10,
):
    """Retorna top N conteudos por engagement score."""
    from app.database.supabase_client import get_supabase_admin

    try:
        supabase = get_supabase_admin()
        query = (
            supabase.table(TABLES["content_pieces"])
            .select("id,title,platform,content_type,engagement_score,created_at")
            .eq("user_id", user["id"])
        )
        if platform:
            query = query.eq("platform", platform)

        result = query.order("engagement_score", desc=True).limit(limit).execute()
        return {"content": result.data or []}
    except Exception as e:
        logger.error(f"Error fetching top content: {e}")
        return {"content": []}
