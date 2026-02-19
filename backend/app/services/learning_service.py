from app.constants import TABLES
from app.database.supabase_client import get_supabase, get_supabase_admin
from datetime import datetime, timedelta


async def analyze_content_patterns(user_id: str, platform: str = None) -> dict:
    """Analisa padroes de sucesso nos conteudos do usuario."""
    supabase = get_supabase_admin()

    query = supabase.table(TABLES["content_pieces"]).select("*").eq("user_id", user_id)
    if platform:
        query = query.eq("platform", platform)
    result = query.order("engagement_score", desc=True).limit(50).execute()

    if not result.data:
        return {"patterns": {}, "recommendations": [], "growth": {}}

    contents = result.data
    top_performing = contents[:10]
    low_performing = contents[-10:]

    patterns = {
        "top_content_types": _count_field(top_performing, "content_type"),
        "top_tones": _count_field(top_performing, "tone"),
        "avg_length_top": _avg_length(top_performing),
        "avg_length_low": _avg_length(low_performing),
        "best_posting_days": _count_field(top_performing, "posted_day"),
        "total_analyzed": len(contents),
    }

    # Growth data from analytics snapshots
    growth = await _get_growth_data(supabase, user_id, platform)

    # Auto-generate recommendations
    recommendations = _generate_recommendations(patterns, growth)

    return {
        "patterns": patterns,
        "growth": growth,
        "recommendations": recommendations,
    }


async def _get_growth_data(supabase, user_id: str, platform: str = None) -> dict:
    """Fetch 30-day growth data from analytics_snapshots."""
    try:
        since = (datetime.now() - timedelta(days=30)).isoformat()
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
            return {}

        snapshots = result.data
        first = snapshots[0]
        last = snapshots[-1]

        return {
            "followers_change": (last.get("followers_count", 0) or 0) - (first.get("followers_count", 0) or 0),
            "avg_engagement": round(
                sum(s.get("engagement_rate", 0) or 0 for s in snapshots) / len(snapshots), 4
            ),
            "avg_reach": round(
                sum(s.get("reach", 0) or 0 for s in snapshots) / len(snapshots)
            ),
            "total_snapshots": len(snapshots),
        }
    except Exception:
        return {}


def _generate_recommendations(patterns: dict, growth: dict) -> list[str]:
    """Generate automatic recommendations based on patterns and growth."""
    recs = []

    top_types = patterns.get("top_content_types", {})
    if top_types:
        best_type = max(top_types, key=top_types.get)
        recs.append(f"Seu tipo de conteudo com melhor performance e '{best_type}'. Aumente a frequencia desse formato.")

    if patterns.get("avg_length_top", 0) > patterns.get("avg_length_low", 0) * 1.5:
        recs.append("Conteudos mais longos e detalhados tendem a performar melhor no seu perfil.")
    elif patterns.get("avg_length_low", 0) > patterns.get("avg_length_top", 0) * 1.5:
        recs.append("Conteudos mais curtos e diretos tendem a performar melhor no seu perfil.")

    followers_change = growth.get("followers_change", 0)
    if followers_change > 0:
        recs.append(f"Crescimento positivo de {followers_change} seguidores nos ultimos 30 dias. Continue assim!")
    elif followers_change < 0:
        recs.append(f"Queda de {abs(followers_change)} seguidores nos ultimos 30 dias. Revise sua estrategia de conteudo.")

    avg_engagement = growth.get("avg_engagement", 0)
    if avg_engagement > 0.05:
        recs.append(f"Taxa de engajamento media de {avg_engagement:.2%} esta excelente (acima de 5%).")
    elif avg_engagement > 0.02:
        recs.append(f"Taxa de engajamento media de {avg_engagement:.2%} esta boa. Tente aumentar com mais CTAs.")
    elif avg_engagement > 0:
        recs.append(f"Taxa de engajamento media de {avg_engagement:.2%} esta abaixo do ideal. Foque em conteudo interativo.")

    if not recs:
        recs.append("Continue postando regularmente para acumular dados de performance.")

    return recs


def _count_field(items: list, field: str) -> dict:
    counts = {}
    for item in items:
        val = item.get(field, "unknown")
        counts[val] = counts.get(val, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def _avg_length(items: list) -> int:
    if not items:
        return 0
    lengths = [len(item.get("body", "")) for item in items]
    return round(sum(lengths) / len(lengths))
