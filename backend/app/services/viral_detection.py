from datetime import datetime, timedelta
from collections import Counter
import logging

logger = logging.getLogger("agentesocial.viral_detection")


def calculate_virality_score(
    likes: int,
    comments: int,
    shares: int,
    saves: int,
    views: int,
    posted_at: datetime,
    followers: int,
) -> dict:
    """
    Calcula score de viralidade de um conteudo.

    Formula: velocidade_engajamento (40%) + taxa_compartilhamento (30%) + taxa_salvamento (30%)

    Score 0-100:
      0-30: Normal
      31-60: Acima da media
      61-80: Viral
      81-100: Super viral
    """
    hours_since_post = max((datetime.utcnow() - posted_at).total_seconds() / 3600, 1)

    total_engagement = likes + comments + shares + saves
    engagement_rate = (total_engagement / max(followers, 1)) * 100

    # Velocidade de engajamento (engajamento/hora normalizado)
    engagement_velocity = total_engagement / hours_since_post
    velocity_score = min(engagement_velocity / max(followers * 0.01, 1) * 100, 100)

    # Taxa de compartilhamento
    share_rate = (shares / max(total_engagement, 1)) * 100
    share_score = min(share_rate * 5, 100)  # 20% share rate = 100 score

    # Taxa de salvamento
    save_rate = (saves / max(total_engagement, 1)) * 100
    save_score = min(save_rate * 5, 100)  # 20% save rate = 100 score

    # Score final ponderado
    final_score = round(
        velocity_score * 0.4 + share_score * 0.3 + save_score * 0.3, 1
    )

    # Classificacao
    if final_score >= 81:
        classification = "super_viral"
    elif final_score >= 61:
        classification = "viral"
    elif final_score >= 31:
        classification = "above_average"
    else:
        classification = "normal"

    return {
        "virality_score": final_score,
        "classification": classification,
        "engagement_rate": round(engagement_rate, 2),
        "velocity_score": round(velocity_score, 1),
        "share_score": round(share_score, 1),
        "save_score": round(save_score, 1),
        "hours_since_post": round(hours_since_post, 1),
        "total_engagement": total_engagement,
    }


def classify_content_batch(items: list) -> list[dict]:
    """
    Classifica uma lista de conteudos por viralidade em lote.

    Cada item no list deve conter:
    - likes (int)
    - comments (int)
    - shares (int)
    - saves (int)
    - views (int)
    - posted_at (datetime or ISO string)
    - followers (int)
    - id (str, optional) - identificador do conteudo
    - caption (str, optional) - texto do post

    Returns:
        Lista de dicts com score de viralidade, ordenada do mais viral ao menos viral.
    """
    results = []

    for idx, item in enumerate(items):
        try:
            # Parse posted_at if it's a string
            posted_at = item.get("posted_at")
            if isinstance(posted_at, str):
                posted_at = datetime.fromisoformat(posted_at.replace("Z", "+00:00").replace("+00:00", ""))
            elif posted_at is None:
                posted_at = datetime.utcnow()

            score_data = calculate_virality_score(
                likes=int(item.get("likes", 0)),
                comments=int(item.get("comments", 0)),
                shares=int(item.get("shares", 0)),
                saves=int(item.get("saves", 0)),
                views=int(item.get("views", 0)),
                posted_at=posted_at,
                followers=int(item.get("followers", 1)),
            )

            # Add original item metadata
            score_data["content_id"] = item.get("id", f"item_{idx}")
            score_data["caption"] = item.get("caption", "")[:200]
            score_data["platform"] = item.get("platform", "unknown")
            score_data["media_type"] = item.get("media_type", "unknown")

            results.append(score_data)

        except Exception as e:
            logger.warning(f"Error classifying item {idx}: {e}")
            results.append({
                "content_id": item.get("id", f"item_{idx}"),
                "virality_score": 0,
                "classification": "error",
                "error": str(e),
            })

    # Sort by virality score descending
    results.sort(key=lambda x: x.get("virality_score", 0), reverse=True)
    return results


def detect_trending_patterns(content_list: list) -> dict:
    """
    Analisa uma lista de conteudos e detecta padroes de tendencias e viralidade.

    Cada item no content_list deve conter:
    - likes (int)
    - comments (int)
    - shares (int)
    - saves (int)
    - views (int)
    - posted_at (datetime or ISO string)
    - followers (int)
    - media_type (str, optional) - tipo de midia (IMAGE, VIDEO, CAROUSEL_ALBUM, etc.)
    - caption (str, optional) - texto do post
    - hashtags (list[str], optional) - hashtags usadas
    - platform (str, optional) - plataforma de origem

    Returns:
        Dict com analise de padroes incluindo:
        - top_performing_type: tipo de midia com melhor desempenho
        - viral_content_ratio: percentual de conteudo classificado como viral+
        - engagement_patterns: padroes de engajamento identificados
        - trending_hashtags: hashtags mais presentes em conteudo viral
        - timing_analysis: melhores horarios/dias para publicar
        - content_recommendations: recomendacoes baseadas nos padroes
    """
    if not content_list:
        return {"error": "Lista de conteudos vazia", "patterns": {}}

    # First, classify all content
    classified = classify_content_batch(content_list)

    # Separate viral and non-viral
    viral_items = [c for c in classified if c.get("classification") in ("viral", "super_viral")]
    above_avg_items = [c for c in classified if c.get("classification") == "above_average"]
    normal_items = [c for c in classified if c.get("classification") == "normal"]

    total = len(classified)
    viral_ratio = len(viral_items) / max(total, 1) * 100

    # Analyze media types
    media_type_scores: dict[str, list] = {}
    for item in classified:
        mt = item.get("media_type", "unknown")
        if mt not in media_type_scores:
            media_type_scores[mt] = []
        media_type_scores[mt].append(item.get("virality_score", 0))

    media_type_avg = {}
    for mt, scores in media_type_scores.items():
        media_type_avg[mt] = round(sum(scores) / len(scores), 1)

    top_media_type = max(media_type_avg, key=media_type_avg.get) if media_type_avg else "unknown"

    # Analyze hashtags in viral content
    viral_hashtags: list[str] = []
    normal_hashtags: list[str] = []
    for idx, item in enumerate(content_list):
        tags = item.get("hashtags", [])
        classification = classified[idx].get("classification", "normal") if idx < len(classified) else "normal"
        if classification in ("viral", "super_viral"):
            viral_hashtags.extend(tags)
        else:
            normal_hashtags.extend(tags)

    viral_hashtag_counts = Counter(viral_hashtags).most_common(10)
    normal_hashtag_counts = Counter(normal_hashtags)

    # Find hashtags that appear disproportionately in viral content
    trending_hashtags = []
    for tag, viral_count in viral_hashtag_counts:
        normal_count = normal_hashtag_counts.get(tag, 0)
        viral_frequency = viral_count / max(len(viral_items), 1)
        normal_frequency = normal_count / max(len(normal_items), 1)
        lift = viral_frequency / max(normal_frequency, 0.01)
        trending_hashtags.append({
            "hashtag": tag,
            "viral_count": viral_count,
            "lift_vs_normal": round(lift, 2),
        })

    trending_hashtags.sort(key=lambda x: x["lift_vs_normal"], reverse=True)

    # Analyze timing patterns
    timing_analysis = {"best_hours": {}, "best_days": {}}
    hour_scores: dict[int, list] = {}
    day_scores: dict[str, list] = {}

    for idx, item in enumerate(content_list):
        posted_at = item.get("posted_at")
        if isinstance(posted_at, str):
            try:
                posted_at = datetime.fromisoformat(posted_at.replace("Z", "+00:00").replace("+00:00", ""))
            except (ValueError, TypeError):
                continue
        elif not isinstance(posted_at, datetime):
            continue

        score = classified[idx].get("virality_score", 0) if idx < len(classified) else 0
        hour = posted_at.hour
        day_name = posted_at.strftime("%A")

        if hour not in hour_scores:
            hour_scores[hour] = []
        hour_scores[hour].append(score)

        if day_name not in day_scores:
            day_scores[day_name] = []
        day_scores[day_name].append(score)

    for hour, scores in hour_scores.items():
        timing_analysis["best_hours"][f"{hour:02d}:00"] = round(sum(scores) / len(scores), 1)

    for day, scores in day_scores.items():
        timing_analysis["best_days"][day] = round(sum(scores) / len(scores), 1)

    # Sort timing data
    if timing_analysis["best_hours"]:
        timing_analysis["best_hours"] = dict(
            sorted(timing_analysis["best_hours"].items(), key=lambda x: x[1], reverse=True)
        )
    if timing_analysis["best_days"]:
        timing_analysis["best_days"] = dict(
            sorted(timing_analysis["best_days"].items(), key=lambda x: x[1], reverse=True)
        )

    # Engagement pattern analysis
    engagement_patterns = {
        "avg_engagement_rate": round(
            sum(c.get("engagement_rate", 0) for c in classified) / max(total, 1), 2
        ),
        "avg_virality_score": round(
            sum(c.get("virality_score", 0) for c in classified) / max(total, 1), 1
        ),
        "share_driven": sum(1 for c in viral_items if c.get("share_score", 0) > c.get("save_score", 0)),
        "save_driven": sum(1 for c in viral_items if c.get("save_score", 0) > c.get("share_score", 0)),
        "velocity_driven": sum(1 for c in viral_items if c.get("velocity_score", 0) > 60),
    }

    # Generate recommendations
    recommendations = []
    if top_media_type != "unknown":
        recommendations.append(f"Priorize conteudo tipo '{top_media_type}' - melhor media de viralidade ({media_type_avg[top_media_type]})")

    if engagement_patterns["share_driven"] > engagement_patterns["save_driven"]:
        recommendations.append("Seu conteudo viral tende a ser impulsionado por compartilhamentos. Foque em conteudo opinativo, polemico (saudavel) e compartilhavel.")
    elif engagement_patterns["save_driven"] > engagement_patterns["share_driven"]:
        recommendations.append("Seu conteudo viral tende a ser impulsionado por salvamentos. Foque em conteudo educativo, tutoriais e listas uteis.")

    if viral_ratio < 10:
        recommendations.append("Menos de 10% do seu conteudo atinge status viral. Experimente formatos diferentes e hooks mais fortes nos primeiros 3 segundos.")
    elif viral_ratio > 30:
        recommendations.append(f"Excelente taxa de viralidade ({viral_ratio:.0f}%)! Mantenha a estrategia atual e documente os padroes que funcionam.")

    if trending_hashtags:
        top_tags = [t["hashtag"] for t in trending_hashtags[:3]]
        recommendations.append(f"Hashtags com maior correlacao com viralidade: {', '.join(top_tags)}")

    best_hour = list(timing_analysis["best_hours"].keys())[0] if timing_analysis["best_hours"] else None
    best_day = list(timing_analysis["best_days"].keys())[0] if timing_analysis["best_days"] else None
    if best_hour and best_day:
        recommendations.append(f"Melhor horario para publicar: {best_hour} | Melhor dia: {best_day}")

    return {
        "total_analyzed": total,
        "classification_breakdown": {
            "super_viral": sum(1 for c in classified if c.get("classification") == "super_viral"),
            "viral": sum(1 for c in classified if c.get("classification") == "viral"),
            "above_average": len(above_avg_items),
            "normal": len(normal_items),
            "error": sum(1 for c in classified if c.get("classification") == "error"),
        },
        "viral_content_ratio": round(viral_ratio, 1),
        "top_performing_type": top_media_type,
        "media_type_avg_scores": media_type_avg,
        "engagement_patterns": engagement_patterns,
        "trending_hashtags": trending_hashtags[:10],
        "timing_analysis": timing_analysis,
        "recommendations": recommendations,
        "top_viral_content": [
            {
                "content_id": c["content_id"],
                "virality_score": c["virality_score"],
                "classification": c["classification"],
                "caption": c.get("caption", "")[:100],
            }
            for c in classified[:5]
        ],
    }
