"""AGNO tools for content learning and performance analysis."""
import json
import logging
from agno.tools import tool
from app.constants import TABLES
from app.database.supabase_client import get_supabase_admin

logger = logging.getLogger("agentesocial.learning_tools")


@tool(name="analyze_content_performance")
def analyze_content_performance(user_id: str, platform: str = None) -> str:
    """Analisa padroes de performance do conteudo do usuario.

    Args:
        user_id: ID do usuario
        platform: Plataforma opcional para filtrar (instagram, youtube, tiktok, linkedin)

    Returns:
        JSON com padroes de conteudo de sucesso incluindo tipos, tons e horarios
    """
    try:
        from app.services.learning_service import analyze_content_patterns
        import asyncio

        # Run async function in sync context
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = pool.submit(
                    asyncio.run, analyze_content_patterns(user_id, platform)
                ).result()
        else:
            result = asyncio.run(analyze_content_patterns(user_id, platform))

        return json.dumps(result, ensure_ascii=False, default=str)
    except Exception as e:
        logger.error(f"Error analyzing content performance: {e}")
        return json.dumps({"error": str(e), "patterns": []})


@tool(name="get_growth_trajectory")
def get_growth_trajectory(user_id: str, platform: str = None, days: int = 30) -> str:
    """Consulta trajetoria de crescimento do usuario nos ultimos N dias.

    Args:
        user_id: ID do usuario
        platform: Plataforma para filtrar
        days: Numero de dias para analisar (padrao: 30)

    Returns:
        JSON com snapshots de analytics mostrando evolucao de seguidores, alcance e engajamento
    """
    try:
        from datetime import datetime, timedelta
        supabase = get_supabase_admin()

        since = (datetime.now() - timedelta(days=days)).isoformat()
        query = (
            supabase.table(TABLES["analytics_snapshots"])
            .select("*")
            .eq("user_id", user_id)
            .gte("created_at", since)
        )
        if platform:
            query = query.eq("platform", platform)

        result = query.order("created_at").execute()

        if not result.data:
            return json.dumps({"snapshots": [], "summary": "Sem dados de analytics para o periodo"})

        snapshots = result.data
        first = snapshots[0]
        last = snapshots[-1]

        summary = {
            "period_days": days,
            "total_snapshots": len(snapshots),
            "followers_start": first.get("followers_count", 0),
            "followers_end": last.get("followers_count", 0),
            "followers_change": (last.get("followers_count", 0) or 0) - (first.get("followers_count", 0) or 0),
            "avg_engagement": round(
                sum(s.get("engagement_rate", 0) or 0 for s in snapshots) / len(snapshots), 4
            ) if snapshots else 0,
            "avg_reach": round(
                sum(s.get("reach", 0) or 0 for s in snapshots) / len(snapshots)
            ) if snapshots else 0,
        }

        return json.dumps({"snapshots": snapshots[-5:], "summary": summary}, ensure_ascii=False, default=str)
    except Exception as e:
        logger.error(f"Error getting growth trajectory: {e}")
        return json.dumps({"error": str(e), "snapshots": []})


@tool(name="get_engagement_insights")
def get_engagement_insights(user_id: str, platform: str = None) -> str:
    """Compara conteudo de alta vs baixa performance para extrair insights.

    Args:
        user_id: ID do usuario
        platform: Plataforma para filtrar

    Returns:
        JSON com comparacao entre top 20% e bottom 20% de conteudo por engagement
    """
    try:
        supabase = get_supabase_admin()

        query = (
            supabase.table(TABLES["content_pieces"])
            .select("*")
            .eq("user_id", user_id)
        )
        if platform:
            query = query.eq("platform", platform)

        result = query.order("engagement_score", desc=True).limit(50).execute()

        if not result.data or len(result.data) < 5:
            return json.dumps({"insights": "Dados insuficientes. Precisa de pelo menos 5 conteudos para analise."})

        contents = result.data
        cutoff = max(1, len(contents) // 5)
        top = contents[:cutoff]
        bottom = contents[-cutoff:]

        def summarize(items):
            types = {}
            tones = {}
            total_length = 0
            for item in items:
                t = item.get("content_type", "unknown")
                types[t] = types.get(t, 0) + 1
                tone = item.get("tone", "unknown")
                tones[tone] = tones.get(tone, 0) + 1
                total_length += len(item.get("body", ""))
            return {
                "count": len(items),
                "content_types": types,
                "tones": tones,
                "avg_length": round(total_length / len(items)) if items else 0,
                "avg_engagement": round(
                    sum(i.get("engagement_score", 0) or 0 for i in items) / len(items), 2
                ) if items else 0,
            }

        insights = {
            "top_performers": summarize(top),
            "low_performers": summarize(bottom),
            "recommendation": (
                f"Seus melhores conteudos tendem a ser do tipo "
                f"{max(summarize(top)['content_types'], key=summarize(top)['content_types'].get, default='N/A')}. "
                f"Foque mais nesse formato."
            ),
        }

        return json.dumps(insights, ensure_ascii=False, default=str)
    except Exception as e:
        logger.error(f"Error getting engagement insights: {e}")
        return json.dumps({"error": str(e), "insights": {}})


@tool(name="save_learning")
def save_learning(user_id: str, learning_type: str, insight: str) -> str:
    """Salva um aprendizado/insight para uso futuro.

    Args:
        user_id: ID do usuario
        learning_type: Tipo do aprendizado (content_pattern, engagement_insight, growth_insight, strategy)
        insight: Texto descritivo do aprendizado

    Returns:
        Confirmacao de salvamento
    """
    try:
        supabase = get_supabase_admin()

        # Check if learnings table exists in constants, else use a generic approach
        table = TABLES.get("learnings", "social_midia_learnings")

        supabase.table(table).insert({
            "user_id": user_id,
            "learning_type": learning_type,
            "insight": insight,
        }).execute()

        return json.dumps({"status": "saved", "learning_type": learning_type})
    except Exception as e:
        logger.warning(f"Could not save learning (table may not exist): {e}")
        return json.dumps({"status": "skipped", "reason": str(e)})


def get_learning_tools() -> list:
    """Returns all learning tools for agent integration."""
    return [
        analyze_content_performance,
        get_growth_trajectory,
        get_engagement_insights,
        save_learning,
    ]
