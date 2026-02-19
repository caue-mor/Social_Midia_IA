import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_current_user
from app.models.schemas import CalendarEventCreate
from app.constants import TABLES

router = APIRouter()
logger = logging.getLogger("agentesocial.calendar")


# --- Schemas for new endpoints ---

class GeneratePlanRequest(BaseModel):
    period: str = "weekly"  # weekly or monthly
    platforms: list[str] = ["instagram", "youtube", "tiktok", "linkedin"]
    focus_topics: Optional[list[str]] = None
    additional_instructions: Optional[str] = None


class AutomationRuleCreate(BaseModel):
    name: str
    trigger_type: str  # e.g. "scheduled", "content_ready", "engagement_drop"
    trigger_config: Optional[dict] = None
    action_type: str  # e.g. "publish", "notify", "repost"
    action_config: Optional[dict] = None
    platform: Optional[str] = None
    is_active: bool = True


# --- Events CRUD ---


@router.post("/events")
async def create_event(
    request: CalendarEventCreate,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    data = {
        "user_id": user["id"],
        "title": request.title,
        "content_id": request.content_id,
        "platform": request.platform,
        "scheduled_at": request.scheduled_at.isoformat(),
        "status": request.status,
        "notes": request.notes,
    }
    result = supabase.table(TABLES["content_calendar"]).insert(data).execute()
    return {"event": result.data[0] if result.data else None}


@router.get("/events")
async def list_events(
    user: dict = Depends(get_current_user),
    month: str = None,
    platform: str = None,
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    query = supabase.table(TABLES["content_calendar"]).select("*").eq("user_id", user["id"])
    if platform:
        query = query.eq("platform", platform)
    if month:
        # Calcula primeiro dia do mes seguinte para range correto
        year, mo = month.split("-")
        next_mo = int(mo) + 1
        next_year = int(year)
        if next_mo > 12:
            next_mo = 1
            next_year += 1
        next_month = f"{next_year}-{next_mo:02d}-01"
        query = query.gte("scheduled_at", f"{month}-01").lt("scheduled_at", next_month)
    result = query.order("scheduled_at").execute()
    return {"events": result.data}


@router.patch("/events/{event_id}")
async def update_event(
    event_id: str,
    user: dict = Depends(get_current_user),
    status: str = None,
    scheduled_at: str = None,
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    data = {}
    if status:
        data["status"] = status
    if scheduled_at:
        data["scheduled_at"] = scheduled_at
    result = supabase.table(TABLES["content_calendar"]).update(data).eq("id", event_id).eq("user_id", user["id"]).execute()
    return {"event": result.data[0] if result.data else None}


@router.delete("/events/{event_id}")
async def delete_event(
    event_id: str,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    try:
        result = (
            supabase.table(TABLES["content_calendar"])
            .delete()
            .eq("id", event_id)
            .eq("user_id", user["id"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Evento nao encontrado")
        return {"deleted": True, "event_id": event_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting event {event_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar evento")


# --- AI Plan Generation ---


@router.post("/generate-plan")
async def generate_plan(
    request: GeneratePlanRequest,
    user: dict = Depends(get_current_user),
):
    from app.agents.team import get_team_response
    from app.database.supabase_client import get_supabase_admin
    from datetime import date

    platforms_str = ", ".join(request.platforms)
    topics_str = ", ".join(request.focus_topics) if request.focus_topics else None

    # Buscar contexto do perfil Instagram
    profile_context = ""
    try:
        supabase = get_supabase_admin()
        profile = (
            supabase.table(TABLES["profiles"])
            .select("username,platform_user_id")
            .eq("user_id", user["id"])
            .eq("platform", "instagram")
            .eq("is_active", True)
            .limit(1)
            .execute()
        )
        if profile.data:
            username = profile.data[0].get("username", "")
            profile_context = f" O usuario tem perfil Instagram @{username}."
    except Exception:
        pass

    today = date.today().strftime("%d/%m/%Y")

    prompt = (
        f"ACAO OBRIGATORIA: Gere IMEDIATAMENTE um plano editorial {request.period} completo "
        f"para as plataformas: {platforms_str}. Data de hoje: {today}.{profile_context} "
    )
    if topics_str:
        prompt += f"Topicos foco: {topics_str}. "
    else:
        prompt += (
            "Use seu conhecimento de tendencias atuais e pesquise na internet "
            "para definir os melhores topicos do momento. "
        )
    prompt += (
        "NAO faca perguntas. NAO peca mais informacoes. "
        "Consulte o calendario existente para evitar conflitos. "
        "Para cada item, inclua: titulo, plataforma, tipo de conteudo, "
        "data/horario ideal e status 'draft'. "
        "Entregue o plano COMPLETO e PRONTO para uso."
    )
    if request.additional_instructions:
        prompt += f" Instrucoes adicionais: {request.additional_instructions}"

    result = await get_team_response(
        message=prompt,
        user_id=user["id"],
        agent_type="calendar_planner",
        context={
            "period": request.period,
            "platforms": platforms_str,
        },
    )
    return result


# --- Automation Rules ---


@router.get("/automation-rules")
async def list_automation_rules(
    user: dict = Depends(get_current_user),
    is_active: Optional[bool] = None,
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    query = supabase.table(TABLES["automation_rules"]).select("*").eq("user_id", user["id"])
    if is_active is not None:
        query = query.eq("is_active", is_active)
    result = query.order("created_at", desc=True).execute()
    return {"rules": result.data}


@router.post("/automation-rules")
async def create_automation_rule(
    request: AutomationRuleCreate,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    data = {
        "user_id": user["id"],
        "name": request.name,
        "trigger_type": request.trigger_type,
        "trigger_config": request.trigger_config or {},
        "action_type": request.action_type,
        "action_config": request.action_config or {},
        "platform": request.platform,
        "is_active": request.is_active,
    }
    try:
        result = supabase.table(TABLES["automation_rules"]).insert(data).execute()
        return {"rule": result.data[0] if result.data else None}
    except Exception as e:
        logger.error(f"Error creating automation rule: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar regra de automacao")
