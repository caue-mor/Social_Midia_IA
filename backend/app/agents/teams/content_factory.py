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
        share_member_interactions=True,
        members=members,
        description=(
            "Fabrica de conteudo completo para redes sociais. "
            "Coordena criacao de textos, visuais e hashtags de forma integrada. "
            "Use para criar posts, carrosseis, reels, stories e qualquer conteudo textual/visual."
        ),
        instructions=[
            "Voce e o coordenador da Content Factory do AgenteSocial.",
            "Ao receber um pedido de conteudo:",
            "1. Delegue ao Content Writer para criar o texto/legenda.",
            "2. Delegue ao Visual Designer para sugerir o visual (layout, cores, prompt de imagem).",
            "3. Delegue ao Hashtag Hunter para gerar as hashtags otimizadas.",
            "4. Compile tudo em uma resposta unica e coesa.",
            "Responda SEMPRE em portugues brasileiro.",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_memory=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
