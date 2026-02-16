import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.models.schemas import ContentGenerateRequest, ContentResponse
from app.constants import TABLES

router = APIRouter()
logger = logging.getLogger("agentesocial.content")


# ---------------------------------------------------------------------------
# Request schemas for the new endpoints
# ---------------------------------------------------------------------------

class ContentUpdateRequest(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    content_type: Optional[str] = None
    platform: Optional[str] = None
    hashtags: Optional[list[str]] = None
    caption: Optional[str] = None
    visual_suggestion: Optional[str] = None
    status: Optional[str] = None
    metadata: Optional[dict] = None


class ContentScheduleRequest(BaseModel):
    scheduled_at: datetime
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# POST /generate  (existing)
# ---------------------------------------------------------------------------

@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentGenerateRequest,
    user: dict = Depends(get_current_user),
):
    from app.agents.team import get_team_response
    prompt = f"Gere um {request.content_type} para {request.platform}"
    if request.topic:
        prompt += f" sobre: {request.topic}"
    if request.tone:
        prompt += f". Tom: {request.tone}"
    if request.additional_instructions:
        prompt += f". Instrucoes: {request.additional_instructions}"

    result = await get_team_response(
        message=prompt,
        user_id=user["id"],
        agent_type="content_writer",
        context={"content_type": request.content_type, "platform": request.platform},
    )
    return ContentResponse(
        id=result["conversation_id"],
        content_type=request.content_type,
        platform=request.platform,
        body=result["response"],
        hashtags=[],
    )


# ---------------------------------------------------------------------------
# GET /library  (existing)
# ---------------------------------------------------------------------------

@router.get("/library")
async def get_content_library(
    user: dict = Depends(get_current_user),
    content_type: str = None,
    platform: str = None,
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    query = supabase.table(TABLES["content_pieces"]).select("*").eq("user_id", user["id"])
    if content_type:
        query = query.eq("content_type", content_type)
    if platform:
        query = query.eq("platform", platform)
    result = query.order("created_at", desc=True).execute()
    return {"content": result.data}


# ---------------------------------------------------------------------------
# PUT /content/{content_id}  - Update content
# ---------------------------------------------------------------------------

@router.put("/{content_id}")
async def update_content(
    content_id: str,
    request: ContentUpdateRequest,
    user: dict = Depends(get_current_user),
):
    """Update an existing content piece. Only the owner can update."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    # Verify ownership
    existing = (
        supabase.table(TABLES["content_pieces"])
        .select("id, user_id")
        .eq("id", content_id)
        .maybe_single()
        .execute()
    )
    if not existing or not existing.data:
        raise HTTPException(status_code=404, detail="Content not found")
    if existing.data.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this content")

    # Build update payload from non-None fields
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_data["updated_at"] = datetime.utcnow().isoformat()

    try:
        result = (
            supabase.table(TABLES["content_pieces"])
            .update(update_data)
            .eq("id", content_id)
            .execute()
        )
        return {"success": True, "content": result.data[0] if result.data else None}
    except Exception as e:
        logger.error(f"Error updating content {content_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ---------------------------------------------------------------------------
# DELETE /content/{content_id}  - Delete content
# ---------------------------------------------------------------------------

@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    user: dict = Depends(get_current_user),
):
    """Delete a content piece. Only the owner can delete."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    # Verify ownership
    existing = (
        supabase.table(TABLES["content_pieces"])
        .select("id, user_id")
        .eq("id", content_id)
        .maybe_single()
        .execute()
    )
    if not existing or not existing.data:
        raise HTTPException(status_code=404, detail="Content not found")
    if existing.data.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this content")

    try:
        supabase.table(TABLES["content_pieces"]).delete().eq("id", content_id).execute()
        return {"success": True, "message": f"Content {content_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting content {content_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ---------------------------------------------------------------------------
# POST /content/{content_id}/publish  - Mark as published
# ---------------------------------------------------------------------------

@router.post("/{content_id}/publish")
async def publish_content(
    content_id: str,
    user: dict = Depends(get_current_user),
):
    """Mark a content piece as published with current timestamp."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    # Verify ownership
    existing = (
        supabase.table(TABLES["content_pieces"])
        .select("id, user_id, status")
        .eq("id", content_id)
        .maybe_single()
        .execute()
    )
    if not existing or not existing.data:
        raise HTTPException(status_code=404, detail="Content not found")
    if existing.data.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to publish this content")

    now = datetime.utcnow().isoformat()
    try:
        result = (
            supabase.table(TABLES["content_pieces"])
            .update({
                "status": "published",
                "published_at": now,
                "updated_at": now,
            })
            .eq("id", content_id)
            .execute()
        )
        return {"success": True, "content": result.data[0] if result.data else None}
    except Exception as e:
        logger.error(f"Error publishing content {content_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ---------------------------------------------------------------------------
# POST /content/{content_id}/schedule  - Schedule content
# ---------------------------------------------------------------------------

@router.post("/{content_id}/schedule")
async def schedule_content(
    content_id: str,
    request: ContentScheduleRequest,
    user: dict = Depends(get_current_user),
):
    """Schedule a content piece for future publishing."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    # Verify ownership
    existing = (
        supabase.table(TABLES["content_pieces"])
        .select("id, user_id, platform")
        .eq("id", content_id)
        .maybe_single()
        .execute()
    )
    if not existing or not existing.data:
        raise HTTPException(status_code=404, detail="Content not found")
    if existing.data.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to schedule this content")

    # Compare as naive UTC datetimes
    scheduled_naive = request.scheduled_at.replace(tzinfo=None) if request.scheduled_at.tzinfo else request.scheduled_at
    if scheduled_naive <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")

    now = datetime.utcnow().isoformat()
    try:
        # Update content piece status
        result = (
            supabase.table(TABLES["content_pieces"])
            .update({
                "status": "scheduled",
                "scheduled_at": request.scheduled_at.isoformat(),
                "updated_at": now,
            })
            .eq("id", content_id)
            .execute()
        )

        # Also create a calendar entry for visibility
        try:
            supabase.table(TABLES["content_calendar"]).insert({
                "user_id": user["id"],
                "content_id": content_id,
                "platform": existing.data.get("platform", ""),
                "scheduled_at": request.scheduled_at.isoformat(),
                "status": "scheduled",
                "notes": request.notes or "",
            }).execute()
        except Exception as cal_err:
            logger.warning(f"Failed to create calendar entry for {content_id}: {cal_err}")

        return {
            "success": True,
            "content": result.data[0] if result.data else None,
            "scheduled_at": request.scheduled_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scheduling content {content_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
