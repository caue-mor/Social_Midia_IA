"""Operations — Sub-team mode=coordinate.

Decompoe tarefas operacionais (calendario, relatorios, memoria).
Membros: Calendar Planner + Report Generator + Memory Agent.
"""

import logging
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

from app.agents.memory_config import create_db, create_memory_manager

logger = logging.getLogger("agentesocial.teams.operations")


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


def create_operations_team() -> Team:
    """Cria o sub-team Operations (coordinate)."""
    from app.agents.calendar_planner import create_calendar_planner
    from app.agents.report_generator import create_report_generator
    from app.agents.memory_agent import create_memory_agent

    members = [
        _safe_create(create_calendar_planner, "Calendar Planner"),
        _safe_create(create_report_generator, "Report Generator"),
        _safe_create(create_memory_agent, "Memory Agent"),
    ]

    return Team(
        name="Operations",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        share_member_interactions=True,
        members=members,
        description=(
            "Equipe de operacoes e gestao. "
            "Gerencia calendario editorial, gera relatorios de performance e mantem memoria/contexto. "
            "Use para calendario, planejamento editorial, relatorios, historico e preferencias."
        ),
        instructions=[
            "Voce e o coordenador de Operations do AgenteSocial.",
            "Ao receber um pedido operacional:",
            "1. Se envolver calendario/planejamento: delegue ao Calendar Planner.",
            "2. Se envolver relatorios/metricas: delegue ao Report Generator.",
            "3. Se envolver memoria/contexto/preferencias: delegue ao Memory Agent.",
            "4. Se envolver multiplas areas, coordene os agentes relevantes.",
            "Responda SEMPRE em portugues brasileiro.",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_memory=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
