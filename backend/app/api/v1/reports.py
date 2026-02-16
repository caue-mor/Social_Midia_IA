import logging
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.models.schemas import ReportGenerateRequest
from app.constants import TABLES

router = APIRouter()
logger = logging.getLogger("agentesocial.reports")


@router.post("/generate")
async def generate_report(
    request: ReportGenerateRequest,
    user: dict = Depends(get_current_user),
):
    from app.agents.team import get_team_response
    from app.database.supabase_client import get_supabase

    sections_str = ", ".join(request.include_sections)
    prompt = (
        f"Gere um relatorio {request.report_type} do periodo {request.period_start} a {request.period_end}. "
        f"Secoes solicitadas: {sections_str}. "
        f"Consulte as tabelas social_midia_content_pieces e social_midia_analytics_snapshots "
        f"para dados reais do usuario. Compare com o periodo anterior quando possivel."
    )

    result = await get_team_response(
        message=prompt,
        user_id=user["id"],
        agent_type="report_generator",
        context={"report_type": request.report_type},
    )

    # Save report to Supabase
    report_content = result.get("response", "")
    if report_content:
        try:
            supabase = get_supabase()
            report_data = {
                "user_id": user["id"],
                "type": request.report_type,
                "title": f"Relatorio {request.report_type.capitalize()} - {request.period_start} a {request.period_end}",
                "content": report_content,
                "period_start": request.period_start,
                "period_end": request.period_end,
                "sections": request.include_sections,
                "metadata": {
                    "agent_type": "report_generator",
                    "conversation_id": result.get("conversation_id"),
                },
            }
            save_result = supabase.table(TABLES["reports"]).insert(report_data).execute()
            if save_result.data:
                result["report_id"] = save_result.data[0].get("id")
                result["report"] = save_result.data[0]
        except Exception as e:
            logger.warning(f"Failed to save report: {e}")

    return result


@router.get("/")
async def list_reports(
    user: dict = Depends(get_current_user),
    report_type: str = None,
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    query = supabase.table(TABLES["reports"]).select("*").eq("user_id", user["id"])
    if report_type:
        query = query.eq("type", report_type)
    result = query.order("created_at", desc=True).execute()
    return {"reports": result.data}


@router.get("/{report_id}")
async def get_report(
    report_id: str,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    try:
        result = (
            supabase.table(TABLES["reports"])
            .select("*")
            .eq("id", report_id)
            .eq("user_id", user["id"])
            .maybe_single()
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Relatorio nao encontrado")
        return {"report": result.data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar relatorio")


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    try:
        result = (
            supabase.table(TABLES["reports"])
            .delete()
            .eq("id", report_id)
            .eq("user_id", user["id"])
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Relatorio nao encontrado")
        return {"deleted": True, "report_id": report_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar relatorio")
