"""Prompt de auditoria de perfil social — v1."""

PROMPT_VERSION = "v1"


def build_prompt(
    user_id: str,
    platforms: list[str],
    focus_topics: list[str] | None = None,
) -> str:
    platforms_str = ", ".join(platforms)
    topics_str = ", ".join(focus_topics) if focus_topics else "tendencias atuais do nicho"

    return (
        f"Realize uma auditoria COMPLETA do perfil social do usuario (user_id: {user_id}) "
        f"nas plataformas: {platforms_str}.\n\n"
        f"Topicos foco: {topics_str}.\n\n"
        "INSTRUCOES:\n"
        "1. Use web_search() para pesquisar tendencias atuais do nicho e concorrentes.\n"
        "2. Use scrape_instagram_profile(username) para analisar perfis publicos de concorrentes (sem API key).\n"
        "3. Use extract_article() para analisar artigos trending do nicho e extrair dados.\n"
        "4. Use search_trending_content() para descobrir o que esta bombando na plataforma.\n"
        "5. Analise engajamento, frequencia de postagem, melhores horarios, concorrentes com DADOS REAIS.\n"
        "6. Identifique pilares de conteudo atuais e recomende ajustes.\n"
        "7. Liste pontos fortes, fracos e oportunidades baseados em pesquisa real.\n\n"
        "FORMATO DE RESPOSTA:\n"
        "Retorne um JSON com os seguintes campos:\n"
        "- pillars: lista de pilares de conteudo (name, description, percentage, examples)\n"
        "- posting_frequency: dict plataforma -> posts/semana\n"
        "- best_posting_times: dict plataforma -> lista de horarios\n"
        "- engagement_rate: dict plataforma -> taxa como float\n"
        "- competitors: lista de concorrentes (name, platform, followers, engagement_rate, strengths, weaknesses)\n"
        "- strengths: lista de pontos fortes\n"
        "- weaknesses: lista de pontos fracos\n"
        "- opportunities: lista de oportunidades\n"
        "- recommendations: lista de recomendacoes priorizadas\n"
    )
