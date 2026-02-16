import uuid
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

from app.constants import TABLES

logger = logging.getLogger("agentesocial.team")


def _safe_create_agent(creator_fn, name: str):
    """Safely create an agent with graceful degradation."""
    try:
        return creator_fn()
    except Exception as e:
        logger.warning(f"Failed to create agent {name}: {e}")
        return Agent(
            name=name,
            model=OpenAIResponses(id="gpt-4.1-nano"),
            role=f"Agente {name} (modo degradado)",
            description=f"Agente {name} em modo limitado devido a erro de inicializacao.",
            instructions=[
                f"Voce e o agente {name} em modo limitado.",
                "Tente ajudar o usuario com base no seu conhecimento geral.",
                "Responda em portugues brasileiro.",
            ],
            markdown=True,
        )


def create_team() -> Team:
    """Cria o time de agentes no modo Supervisor."""
    from app.agents.master_orchestrator import create_master_agent
    from app.agents.social_analyst import create_social_analyst
    from app.agents.content_writer import create_content_writer
    from app.agents.viral_tracker import create_viral_tracker
    from app.agents.hashtag_hunter import create_hashtag_hunter
    from app.agents.podcast_creator import create_podcast_creator
    from app.agents.video_script_writer import create_video_script_writer
    from app.agents.calendar_planner import create_calendar_planner
    from app.agents.report_generator import create_report_generator
    from app.agents.strategy_advisor import create_strategy_advisor
    from app.agents.visual_designer import create_visual_designer
    from app.agents.memory_agent import create_memory_agent

    members = [
        _safe_create_agent(create_social_analyst, "Social Media Analyst"),
        _safe_create_agent(create_content_writer, "Content Writer"),
        _safe_create_agent(create_viral_tracker, "Viral Content Tracker"),
        _safe_create_agent(create_hashtag_hunter, "Hashtag Hunter"),
        _safe_create_agent(create_podcast_creator, "Podcast Creator"),
        _safe_create_agent(create_video_script_writer, "Video Script Writer"),
        _safe_create_agent(create_calendar_planner, "Calendar Planner"),
        _safe_create_agent(create_report_generator, "Report Generator"),
        _safe_create_agent(create_strategy_advisor, "Strategy Advisor"),
        _safe_create_agent(create_visual_designer, "Visual Designer"),
        _safe_create_agent(create_memory_agent, "Memory Agent"),
    ]

    team = Team(
        name="AgenteSocial Team",
        mode="supervisor",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        members=members,
        description="Time de IA especializado em gestao completa de redes sociais",
        instructions=[
            "Voce e o orquestrador do AgenteSocial, um ecossistema de IA para gestao de redes sociais.",
            "Analise a mensagem do usuario e delegue para o agente especialista mais adequado.",
            "Sempre consulte o Memory Agent para contexto do usuario antes de responder.",
            "Responda SEMPRE em portugues brasileiro.",
            "Se a tarefa envolver multiplos agentes, coordene a execucao sequencial.",
        ],
        show_members_responses=True,
        enable_agentic_memory=True,
        markdown=True,
    )
    return team


# Cache do team
_team: Team = None


def get_team() -> Team:
    global _team
    if _team is None:
        _team = create_team()
    return _team


async def get_team_response(
    message: str,
    user_id: str,
    conversation_id: str = None,
    agent_type: str = None,
    context: dict = None,
) -> dict:
    """Envia mensagem para o team e retorna resposta."""
    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    try:
        team = get_team()

        # Adiciona contexto ao prompt
        full_message = message
        if context:
            context_str = ", ".join(f"{k}: {v}" for k, v in context.items())
            full_message = f"[Contexto: user_id={user_id}, {context_str}] {message}"
        else:
            full_message = f"[Contexto: user_id={user_id}] {message}"

        # Executa o team
        response = team.run(full_message)
        response_text = response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        logger.error(f"Team execution error: {e}")
        response_text = "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente em alguns instantes."

    # Salva conversa no Supabase (non-blocking)
    try:
        from app.database.supabase_client import get_supabase
        supabase = get_supabase()

        existing = supabase.table(TABLES["agent_conversations"]).select("messages").eq("id", conversation_id).maybe_single().execute()
        messages = existing.data["messages"] if existing and existing.data else []
        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response_text})

        if existing and existing.data:
            supabase.table(TABLES["agent_conversations"]).update({
                "messages": messages,
                "updated_at": "now()",
            }).eq("id", conversation_id).execute()
        else:
            supabase.table(TABLES["agent_conversations"]).insert({
                "id": conversation_id,
                "user_id": user_id,
                "agent_type": agent_type or "master",
                "messages": messages,
            }).execute()
    except Exception as e:
        logger.warning(f"Failed to save conversation: {e}")

    return {
        "response": response_text,
        "conversation_id": conversation_id,
        "agent_type": agent_type or "master",
        "metadata": context,
    }
