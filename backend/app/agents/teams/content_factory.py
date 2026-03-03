"""Content Factory — Sub-team mode=coordinate.

Coordena criacao de conteudo completo: texto + visual + hashtags.
Membros: Content Writer + Visual Designer + Hashtag Hunter.
"""

import logging
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

from app.agents.memory_config import create_db, create_memory_manager

logger = logging.getLogger("agentesocial.teams.content_factory")


def _safe_create(creator_fn, name: str):
    try:
        return creator_fn()
    except Exception as e:
        logger.warning(f"Failed to create agent {name}: {e}")
        return Agent(
            name=name,
            model=OpenAIResponses(id="gpt-4.1-nano"),
            role=f"Agente {name} (modo degradado)",
            instructions=["Responda em portugues brasileiro."],
            markdown=True,
        )


def create_content_factory() -> Team:
    """Cria o sub-team Content Factory (coordinate)."""
    from app.agents.content_writer import create_content_writer
    from app.agents.visual_designer import create_visual_designer
    from app.agents.hashtag_hunter import create_hashtag_hunter

    members = [
        _safe_create(create_content_writer, "Content Writer"),
        _safe_create(create_visual_designer, "Visual Designer"),
        _safe_create(create_hashtag_hunter, "Hashtag Hunter"),
    ]

    return Team(
        name="Content Factory",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        share_member_interactions=False,
        members=members,
        description=(
            "Fabrica de conteudo completo para redes sociais. "
            "Coordena criacao de textos, visuais e hashtags de forma integrada. "
            "Use para criar posts, carrosseis, reels, stories e qualquer conteudo textual/visual."
        ),
        instructions=[
            "REGRA CRITICA: Voce e o coordenador da Content Factory. "
            "NUNCA faca perguntas ao usuario. NUNCA diga 'vou delegar' ou 'vou coordenar'. "
            "EXECUTE imediatamente delegando aos membros e compilando a resposta final.",
            "",
            "REGRA ANTI-META: "
            "NUNCA entregue uma resposta que DESCREVE o que seria feito. "
            "NUNCA liste topicos ou temas sem o conteudo real escrito. "
            "NUNCA diga 'preparei um plano que engloba' seguido de bullet points vagos. "
            "NUNCA termine com 'se desejar posso criar' ou 'posso seguir criando'. "
            "A resposta final DEVE conter conteudo REAL, ESCRITO, PRONTO para publicar.",
            "",
            "FLUXO OBRIGATORIO (execute em sequencia, sem perguntar):",
            "1. Delegue ao Content Writer: 'Escreva AGORA os posts, stories, reels e frases COMPLETOS com texto real. NAO descreva o que faria — ESCREVA o conteudo.'",
            "2. Delegue ao Visual Designer: 'Crie sugestoes visuais com paleta de cores, dimensoes e prompts DALL-E prontos.'",
            "3. Delegue ao Hashtag Hunter: 'Gere as hashtags organizadas por volume (alto/medio/nicho) com exemplos reais.'",
            "4. Compile TUDO em uma resposta unica e entregue ao usuario.",
            "",
            "Se um membro retornar uma descricao vaga em vez de conteudo real, REJEITE e peca para reescrever com conteudo concreto. "
            "Se um membro falhar, continue com os outros e entregue o que tiver.",
            "",
            "Responda SEMPRE em portugues brasileiro.",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_memory=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
