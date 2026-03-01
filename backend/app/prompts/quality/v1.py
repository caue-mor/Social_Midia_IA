"""Prompt de quality gate — v1."""

import json

PROMPT_VERSION = "v1"


def build_prompt(
    content_items: list[dict],
    plan_slots: list[dict] | None = None,
) -> str:
    content_json = json.dumps(content_items, ensure_ascii=False, indent=2)

    plan_ctx = ""
    if plan_slots:
        plan_ctx = (
            f"Plano editorial original ({len(plan_slots)} slots):\n"
            f"{json.dumps(plan_slots, ensure_ascii=False, indent=2)}\n\n"
        )

    return (
        "Realize uma validacao de qualidade COMPLETA do conteudo gerado abaixo.\n\n"
        f"{plan_ctx}"
        f"Conteudo para validar ({len(content_items)} pecas):\n"
        f"{content_json}\n\n"
        "EXECUTE OS 7 CHECKS:\n"
        "1. CTA presente: fail se sem CTA, warn se generico\n"
        "2. Hook: fail se sem hook, warn se fraco\n"
        "3. Hashtags 30/40/30: fail se sem hashtags, warn se fora proporcao\n"
        "4. Repeticao de temas: use get_content_history para verificar. "
        "fail se tema repetido <3 dias, warn se 4-7 dias\n"
        "5. Adequacao ao tempo: fail se >3 posts/dia na mesma plataforma, warn se conflito horario\n"
        "6. Contagem palavras por plataforma: fail se excede limite, warn se abaixo do ideal\n"
        "   (Instagram max 2200, LinkedIn max 3000, Twitter max 280, TikTok max 300)\n"
        "7. Secoes obrigatorias por tipo: fail se ausente, warn se recomendada ausente\n"
        "   (Post: hook+body+cta, Carrossel: 7 slides, Reel: hook+blocks+cta)\n\n"
        "CRITERIOS DE VEREDICTO:\n"
        "- passed: score >= 80 (nenhum check fail)\n"
        "- warn: score 50-79 (apenas warns, nenhum fail)\n"
        "- fail: score < 50 (algum check falhou)\n\n"
        "Score: inicie em 100, subtraia 15 por fail e 5 por warn.\n\n"
        "FORMATO DE RESPOSTA:\n"
        "Retorne JSON com:\n"
        "- verdict: 'passed', 'warn' ou 'fail'\n"
        "- score: int de 0 a 100\n"
        "- checks: lista de QualityCheck (name, passed, severity, message, details)\n"
        "- summary: resumo geral em 2-3 frases\n"
        "- recommendations: lista de recomendacoes para melhorar\n"
    )
