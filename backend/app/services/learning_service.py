from app.constants import TABLES
from app.database.supabase_client import get_supabase


async def analyze_content_patterns(user_id: str, platform: str = None) -> dict:
    """Analisa padroes de sucesso nos conteudos do usuario."""
    supabase = get_supabase()

    query = supabase.table(TABLES["content_pieces"]).select("*").eq("user_id", user_id)
    if platform:
        query = query.eq("platform", platform)
    result = query.order("engagement_score", desc=True).limit(50).execute()

    if not result.data:
        return {"patterns": [], "recommendations": []}

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

    return patterns


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
