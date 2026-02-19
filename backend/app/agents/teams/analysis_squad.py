"""Analysis Squad — Sub-team mode=coordinate.

Todos analisam e o lider sintetiza insights.
Membros: Social Analyst + Viral Tracker + Strategy Advisor.
"""

import logging
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

from app.agents.memory_config import create_db, create_memory_manager

logger = logging.getLogger("agentesocial.teams.analysis_squad")


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


def create_analysis_squad() -> Team:
    """Cria o sub-team Analysis Squad (coordinate)."""
    from app.agents.social_analyst import create_social_analyst
    from app.agents.viral_tracker import create_viral_tracker
    from app.agents.strategy_advisor import create_strategy_advisor

    members = [
        _safe_create(create_social_analyst, "Social Media Analyst"),
        _safe_create(create_viral_tracker, "Viral Content Tracker"),
        _safe_create(create_strategy_advisor, "Strategy Advisor"),
    ]

    return Team(
        name="Analysis Squad",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        share_member_interactions=True,
        members=members,
        description=(
            "Esquadrao de analise e inteligencia de redes sociais. "
            "Analisa metricas, detecta tendencias virais e define estrategias. "
            "Use para analise de perfil, metricas, tendencias, viral, benchmarking e consultoria estrategica."
        ),
        instructions=[
            "REGRA: Instrua os membros a usarem suas ferramentas PROATIVAMENTE. "
            "Nenhum membro deve fazer perguntas ao usuario — todos devem buscar dados e agir imediatamente.",
            "",
            "Voce e o coordenador do Analysis Squad do AgenteSocial.",
            "Ao receber um pedido de analise:",
            "1. Delegue ao Social Media Analyst para dados de perfil e metricas.",
            "2. Delegue ao Viral Content Tracker para tendencias e oportunidades virais.",
            "3. Delegue ao Strategy Advisor para recomendacoes estrategicas.",
            "4. Sintetize os insights em uma resposta unificada com acoes concretas.",
            "Responda SEMPRE em portugues brasileiro.",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_memory=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
