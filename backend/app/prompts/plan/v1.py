"""Prompt de plano editorial — v1."""

PROMPT_VERSION = "v1"


def build_prompt(
    audit_summary: dict,
    period: str,
    platforms: list[str],
    focus_topics: list[str] | None = None,
) -> str:
    platforms_str = ", ".join(platforms)
    topics_str = ", ".join(focus_topics) if focus_topics else "baseado na auditoria"

    pillars_str = ""
    if audit_summary.get("pillars"):
        pillars_str = "Pilares identificados na auditoria: " + ", ".join(
            p.get("name", "") for p in audit_summary["pillars"] if p.get("name")
        ) + ".\n"

    recommendations_str = ""
    if audit_summary.get("recommendations"):
        recommendations_str = "Recomendacoes da auditoria: " + "; ".join(
            audit_summary["recommendations"][:5]
        ) + ".\n"

    is_monthly = period == "monthly"
    period_desc = "mensal (4 semanas)" if is_monthly else "semanal (7 dias)"

    return (
        f"Gere um plano editorial {period_desc} COMPLETO para as plataformas: {platforms_str}.\n\n"
        f"Topicos foco: {topics_str}.\n"
        f"{pillars_str}"
        f"{recommendations_str}\n"
        "INSTRUCOES:\n"
        "1. Consulte o calendario existente para evitar conflitos.\n"
        "2. Use os melhores horarios por plataforma.\n"
        "3. Distribua conteudo: 40% educativo, 30% entretenimento, 20% vendas, 10% institucional.\n"
        "4. Varie formatos (post, carrossel, reel, story, thread, video).\n"
        "5. Considere datas sazonais brasileiras do periodo.\n\n"
        "FORMATO DE RESPOSTA:\n"
        + (
            "Retorne JSON com:\n"
            "- month: string do mes (ex: '2026-03')\n"
            "- year: int\n"
            "- weeks: lista de objetos WeeklyPlan, cada um com:\n"
            "  - week_number, start_date, end_date\n"
            "  - slots: lista de PlanSlot (title, platform, content_type, scheduled_date, scheduled_time, topic, pillar, notes, status)\n"
            "  - total_posts, platforms_covered\n"
            "- total_posts: int total do mes\n"
            "- seasonal_dates: lista de datas sazonais\n"
            if is_monthly else
            "Retorne JSON com:\n"
            "- week_number: int\n"
            "- start_date: string (YYYY-MM-DD)\n"
            "- end_date: string (YYYY-MM-DD)\n"
            "- slots: lista de PlanSlot, cada um com: title, platform, content_type, "
            "scheduled_date, scheduled_time, topic, pillar, notes, status='draft'\n"
            "- total_posts: int\n"
            "- platforms_covered: lista de plataformas\n"
        )
    )
