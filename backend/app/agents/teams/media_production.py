"""Media Production — Sub-team mode=coordinate.

Coordena producao de conteudo de audio e video.
Membros: Podcast Creator + Video Script Writer.
"""

import logging
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

from app.agents.memory_config import create_db, create_memory_manager

logger = logging.getLogger("agentesocial.teams.media_production")


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


def create_media_production() -> Team:
    """Cria o sub-team Media Production (coordinate)."""
    from app.agents.podcast_creator import create_podcast_creator
    from app.agents.video_script_writer import create_video_script_writer

    members = [
        _safe_create(create_podcast_creator, "Podcast Creator"),
        _safe_create(create_video_script_writer, "Video Script Writer"),
    ]

    return Team(
        name="Media Production",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        share_member_interactions=True,
        members=members,
        description=(
            "Equipe de producao de midia (audio e video). "
            "Cria roteiros de podcast, show notes, roteiros de video (Reels, TikTok, YouTube). "
            "Use para podcasts, roteiros de video, scripts, show notes e clips."
        ),
        instructions=[
            "Voce e o coordenador do Media Production do AgenteSocial.",
            "Ao receber um pedido de midia:",
            "1. Se envolver podcast: delegue ao Podcast Creator.",
            "2. Se envolver video (Reels, TikTok, YouTube): delegue ao Video Script Writer.",
            "3. Se envolver ambos (ex: podcast com clips para Reels): coordene os dois.",
            "4. Compile a resposta em formato profissional e pronto para producao.",
            "Responda SEMPRE em portugues brasileiro.",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_memory=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
