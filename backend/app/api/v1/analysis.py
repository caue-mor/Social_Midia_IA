import logging
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_current_user
from app.models.schemas import ProfileAnalysisRequest, TrendSearchRequest
from app.constants import TABLES

logger = logging.getLogger("agentesocial.analysis")

router = APIRouter()


class CompetitorAnalysisRequest(BaseModel):
    platform: str
    my_handle: str
    competitor_handles: list[str]
    metrics: list[str] = ["engagement_rate", "posting_frequency", "content_mix", "growth"]


@router.post("/profile")
async def analyze_profile(
    request: ProfileAnalysisRequest,
    user: dict = Depends(get_current_user),
):
    from app.agents.team import get_team_response
    prompt = f"Analise o perfil @{request.profile_handle} no {request.platform}. Forneca metricas, pontos fortes, fracos e recomendacoes."
    result = await get_team_response(
        message=prompt,
        user_id=user["id"],
        agent_type="social_analyst",
        context={"platform": request.platform, "handle": request.profile_handle},
    )
    return result


@router.post("/trends")
async def search_trends(
    request: TrendSearchRequest,
    user: dict = Depends(get_current_user),
):
    from app.agents.team import get_team_response
    keywords_str = ", ".join(request.keywords)
    prompt = f"Pesquise tendencias para: {keywords_str}. Pais: {request.country}."
    if request.platform:
        prompt += f" Plataforma: {request.platform}."
    result = await get_team_response(
        message=prompt,
        user_id=user["id"],
        agent_type="trend_analyst",
        context={"keywords": request.keywords},
    )
    return result


@router.get("/viral")
async def get_viral_content(
    user: dict = Depends(get_current_user),
    platform: str = None,
    niche: str = None,
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    query = supabase.table(TABLES["viral_content"]).select("*").gte("virality_score", 70)
    if platform:
        query = query.eq("platform", platform)
    if niche:
        query = query.eq("niche", niche)
    result = query.order("virality_score", desc=True).limit(50).execute()
    return {"viral_content": result.data}


@router.post("/competitor")
async def analyze_competitor(
    request: CompetitorAnalysisRequest,
    user: dict = Depends(get_current_user),
):
    """Analisa concorrentes comparando metricas com o perfil do usuario."""
    from app.agents.team import get_team_response

    competitors_str = ", ".join(f"@{h}" for h in request.competitor_handles)
    metrics_str = ", ".join(request.metrics)
    prompt = (
        f"Faca uma analise competitiva completa no {request.platform}. "
        f"Meu perfil: @{request.my_handle}. "
        f"Concorrentes: {competitors_str}. "
        f"Compare as seguintes metricas: {metrics_str}. "
        f"Identifique gaps, oportunidades e forneca recomendacoes acionaveis "
        f"para superar cada concorrente. Estruture a resposta com uma tabela "
        f"comparativa e um plano de acao priorizado."
    )

    # Save competitor tracking data
    try:
        from app.database.supabase_client import get_supabase
        supabase = get_supabase()
        for handle in request.competitor_handles:
            supabase.table(TABLES["competitor_tracking"]).upsert(
                {
                    "user_id": user["id"],
                    "platform": request.platform,
                    "competitor_handle": handle,
                    "tracking_active": True,
                },
                on_conflict="user_id,platform,competitor_handle",
            ).execute()
    except Exception as e:
        logger.warning(f"Failed to save competitor tracking: {e}")

    result = await get_team_response(
        message=prompt,
        user_id=user["id"],
        agent_type="social_analyst",
        context={
            "platform": request.platform,
            "my_handle": request.my_handle,
            "competitors": request.competitor_handles,
            "metrics": request.metrics,
        },
    )
    return result


@router.get("/benchmarks/{platform}")
async def get_benchmarks(
    platform: str,
    user: dict = Depends(get_current_user),
    niche: Optional[str] = Query(None, description="Nicho para benchmarks especificos (ex: moda, tech, fitness)"),
    account_size: Optional[str] = Query(None, description="Faixa de seguidores: nano, micro, mid, macro, mega"),
):
    """Retorna benchmarks de referencia por plataforma e nicho."""
    # Industry benchmarks by platform and account size
    benchmarks = {
        "instagram": {
            "nano": {"followers": "1K-10K", "engagement_rate": {"low": 3.0, "avg": 5.0, "high": 8.0}, "posts_per_week": {"low": 3, "avg": 5, "high": 7}, "stories_per_day": {"low": 1, "avg": 3, "high": 7}, "reels_per_week": {"low": 2, "avg": 4, "high": 7}},
            "micro": {"followers": "10K-50K", "engagement_rate": {"low": 1.5, "avg": 3.0, "high": 5.0}, "posts_per_week": {"low": 3, "avg": 5, "high": 7}, "stories_per_day": {"low": 2, "avg": 5, "high": 10}, "reels_per_week": {"low": 3, "avg": 5, "high": 7}},
            "mid": {"followers": "50K-500K", "engagement_rate": {"low": 1.0, "avg": 2.0, "high": 3.5}, "posts_per_week": {"low": 4, "avg": 6, "high": 10}, "stories_per_day": {"low": 3, "avg": 7, "high": 15}, "reels_per_week": {"low": 4, "avg": 6, "high": 10}},
            "macro": {"followers": "500K-1M", "engagement_rate": {"low": 0.7, "avg": 1.5, "high": 2.5}, "posts_per_week": {"low": 5, "avg": 7, "high": 14}, "stories_per_day": {"low": 5, "avg": 10, "high": 20}, "reels_per_week": {"low": 5, "avg": 7, "high": 14}},
            "mega": {"followers": "1M+", "engagement_rate": {"low": 0.5, "avg": 1.0, "high": 2.0}, "posts_per_week": {"low": 5, "avg": 7, "high": 14}, "stories_per_day": {"low": 5, "avg": 10, "high": 20}, "reels_per_week": {"low": 5, "avg": 7, "high": 14}},
        },
        "youtube": {
            "nano": {"subscribers": "1K-10K", "view_rate": {"low": 10.0, "avg": 20.0, "high": 40.0}, "like_rate": {"low": 3.0, "avg": 5.0, "high": 8.0}, "comment_rate": {"low": 0.3, "avg": 0.8, "high": 2.0}, "videos_per_month": {"low": 2, "avg": 4, "high": 8}, "avg_retention": {"low": 30, "avg": 45, "high": 60}},
            "micro": {"subscribers": "10K-100K", "view_rate": {"low": 5.0, "avg": 15.0, "high": 30.0}, "like_rate": {"low": 2.0, "avg": 4.0, "high": 7.0}, "comment_rate": {"low": 0.2, "avg": 0.5, "high": 1.5}, "videos_per_month": {"low": 4, "avg": 8, "high": 12}, "avg_retention": {"low": 35, "avg": 48, "high": 60}},
            "mid": {"subscribers": "100K-1M", "view_rate": {"low": 3.0, "avg": 10.0, "high": 20.0}, "like_rate": {"low": 1.5, "avg": 3.5, "high": 6.0}, "comment_rate": {"low": 0.1, "avg": 0.4, "high": 1.0}, "videos_per_month": {"low": 4, "avg": 8, "high": 16}, "avg_retention": {"low": 38, "avg": 50, "high": 65}},
            "macro": {"subscribers": "1M+", "view_rate": {"low": 2.0, "avg": 8.0, "high": 15.0}, "like_rate": {"low": 1.0, "avg": 3.0, "high": 5.0}, "comment_rate": {"low": 0.05, "avg": 0.3, "high": 0.8}, "videos_per_month": {"low": 4, "avg": 8, "high": 16}, "avg_retention": {"low": 40, "avg": 52, "high": 65}},
        },
        "tiktok": {
            "nano": {"followers": "1K-10K", "engagement_rate": {"low": 5.0, "avg": 9.0, "high": 15.0}, "videos_per_week": {"low": 3, "avg": 7, "high": 14}, "avg_watch_time_pct": {"low": 40, "avg": 60, "high": 80}},
            "micro": {"followers": "10K-100K", "engagement_rate": {"low": 3.0, "avg": 6.0, "high": 12.0}, "videos_per_week": {"low": 5, "avg": 10, "high": 21}, "avg_watch_time_pct": {"low": 35, "avg": 55, "high": 75}},
            "mid": {"followers": "100K-1M", "engagement_rate": {"low": 2.0, "avg": 4.5, "high": 9.0}, "videos_per_week": {"low": 5, "avg": 10, "high": 21}, "avg_watch_time_pct": {"low": 35, "avg": 55, "high": 75}},
            "macro": {"followers": "1M+", "engagement_rate": {"low": 1.5, "avg": 3.5, "high": 7.0}, "videos_per_week": {"low": 7, "avg": 14, "high": 28}, "avg_watch_time_pct": {"low": 30, "avg": 50, "high": 70}},
        },
    }

    niche_modifiers = {
        "moda": {"engagement_modifier": 1.1, "notes": "Moda tende a ter engajamento acima da media por apelo visual"},
        "tech": {"engagement_modifier": 0.85, "notes": "Conteudo tech tem engajamento menor mas maior conversao"},
        "fitness": {"engagement_modifier": 1.2, "notes": "Fitness tem alto engajamento, especialmente em Reels/TikTok"},
        "gastronomia": {"engagement_modifier": 1.15, "notes": "Gastronomia performa bem em formatos visuais e curtos"},
        "educacao": {"engagement_modifier": 0.9, "notes": "Educacao tem engajamento menor mas alto salvamento e compartilhamento"},
        "negocios": {"engagement_modifier": 0.8, "notes": "B2B tem menor engajamento mas leads mais qualificados"},
        "beleza": {"engagement_modifier": 1.15, "notes": "Beleza tem alto engajamento com tutoriais e antes/depois"},
        "viagem": {"engagement_modifier": 1.1, "notes": "Viagem performa bem com conteudo aspiracional e carrosseis"},
    }

    platform_lower = platform.lower()
    if platform_lower not in benchmarks:
        return {
            "error": f"Plataforma '{platform}' nao suportada. Opcoes: {list(benchmarks.keys())}",
        }

    platform_data = benchmarks[platform_lower]

    # Filter by account size if specified
    if account_size and account_size in platform_data:
        result_data = {account_size: platform_data[account_size]}
    else:
        result_data = platform_data

    response = {
        "platform": platform_lower,
        "benchmarks": result_data,
    }

    # Add niche modifier if specified
    if niche and niche.lower() in niche_modifiers:
        response["niche"] = niche.lower()
        response["niche_modifier"] = niche_modifiers[niche.lower()]
    elif niche:
        response["niche"] = niche.lower()
        response["niche_modifier"] = {
            "engagement_modifier": 1.0,
            "notes": f"Sem dados especificos para o nicho '{niche}'. Usando benchmarks gerais.",
        }

    return response
