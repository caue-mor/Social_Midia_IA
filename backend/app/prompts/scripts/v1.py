"""Prompt de roteiros de video — v1."""

PROMPT_VERSION = "v1"


def build_prompt(
    slot: dict,
    script_type: str = "reel",
) -> str:
    title = slot.get("title", "")
    platform = slot.get("platform", "")
    topic = slot.get("topic", title)
    pillar = slot.get("pillar", "")
    notes = slot.get("notes", "")

    if script_type == "youtube":
        schema_desc = (
            "Retorne JSON com:\n"
            "- title: titulo SEO (max 60 chars)\n"
            "- title_alt: titulo alternativo clickbait moderado\n"
            "- duration_minutes: duracao estimada\n"
            "- chapters: lista de ScriptChapter (title, timestamp_start, timestamp_end, "
            "speech, visual, b_roll, text_overlay, retention_cue)\n"
            "- description_seo: descricao 200+ palavras\n"
            "- tags: lista de 10-15 tags\n"
            "- thumbnail_brief: descricao do visual da thumbnail\n"
            "- timestamps: lista formatada para descricao\n"
        )
    else:
        schema_desc = (
            "Retorne JSON com:\n"
            "- title: titulo do reel/short\n"
            "- platform: plataforma alvo\n"
            "- duration_seconds: duracao em segundos\n"
            "- hook: frase de hook dos primeiros 2s\n"
            "- blocks: lista de ScriptBlock (timestamp, visual, speech, "
            "text_overlay, effect, notes)\n"
            "- audio_suggestion: sugestao de audio/musica\n"
            "- hashtags: lista de hashtags\n"
            "- caption: legenda completa\n"
        )

    return (
        f"Crie um roteiro completo de video ({script_type}).\n\n"
        f"Plataforma: {platform}\n"
        f"Tema: {topic}\n"
        f"Pilar: {pillar}\n"
        f"Titulo sugerido: {title}\n"
        f"Notas: {notes}\n\n"
        "INSTRUCOES:\n"
        "1. Busque brand voice para adaptar tom e linguagem.\n"
        "2. Hook nos primeiros 2 segundos e OBRIGATORIO.\n"
        "3. Inclua marcadores de edicao ([CORTE], [B-ROLL], [TEXTO], etc).\n"
        "4. Roteiro deve soar natural (conversa, nao leitura).\n"
        "5. Inclua direcoes de performance ([sorrindo], [serio], [empolgado]).\n\n"
        f"FORMATO DE RESPOSTA:\n{schema_desc}"
    )
