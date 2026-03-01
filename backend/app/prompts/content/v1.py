"""Prompt de criacao de conteudo — v1."""

PROMPT_VERSION = "v1"


def build_prompt(
    slot: dict,
    brand_voice_summary: str = "",
) -> str:
    title = slot.get("title", "")
    platform = slot.get("platform", "")
    content_type = slot.get("content_type", "post")
    topic = slot.get("topic", title)
    pillar = slot.get("pillar", "")
    notes = slot.get("notes", "")

    brand_ctx = ""
    if brand_voice_summary:
        brand_ctx = f"Brand voice do usuario: {brand_voice_summary}\nAdapte tom e estilo.\n\n"

    return (
        f"Crie um conteudo completo para publicacao.\n\n"
        f"Plataforma: {platform}\n"
        f"Tipo: {content_type}\n"
        f"Tema: {topic}\n"
        f"Pilar: {pillar}\n"
        f"Titulo sugerido: {title}\n"
        f"Notas: {notes}\n\n"
        f"{brand_ctx}"
        "INSTRUCOES:\n"
        "1. Use web_search() para pesquisar dados recentes sobre o topico e encontrar estatisticas reais.\n"
        "2. Use search_trending_content() para descobrir angles virais e tendencias atuais do tema.\n"
        "3. Busque o brand voice do usuario para adaptar tom.\n"
        "4. Consulte historico para evitar repeticao de temas recentes.\n"
        "5. Siga o template do tipo de conteudo (post, carrossel, reel, etc).\n"
        "6. Inclua hook forte, CTA especifico, hashtags organizadas.\n"
        "7. Inclua dados/estatisticas REAIS pesquisados (nunca invente numeros).\n\n"
        "FORMATO DE RESPOSTA:\n"
        "Retorne JSON com:\n"
        "- title: titulo do conteudo\n"
        "- platform: plataforma alvo\n"
        "- content_type: tipo do conteudo\n"
        "- hook: frase de abertura que prende atencao\n"
        "- body: corpo completo do conteudo\n"
        "- caption: legenda/caption\n"
        "- cta: call to action especifico\n"
        "- hashtags: lista de hashtags\n"
        "- visual_suggestion: descricao do visual ideal\n"
        "- slides: lista de dicts com slides (se carrossel)\n"
        "- story_frames: lista de dicts com frames (se story)\n"
        "- thread_tweets: lista de tweets (se thread)\n"
        "- word_count: contagem de palavras do body\n"
    )
