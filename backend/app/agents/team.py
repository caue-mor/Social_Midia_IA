import uuid
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

from app.constants import TABLES
from app.agents.memory_config import create_db, create_memory_manager

logger = logging.getLogger("agentesocial.team")


def _safe_create_sub_team(creator_fn, name: str):
    """Safely create a sub-team with graceful degradation."""
    try:
        return creator_fn()
    except Exception as e:
        logger.warning(f"Failed to create sub-team {name}: {e}")
        return Agent(
            name=name,
            model=OpenAIResponses(id="gpt-4.1-nano"),
            role=f"Sub-team {name} (modo degradado)",
            description=f"Sub-team {name} em modo limitado devido a erro de inicializacao.",
            instructions=[
                f"Voce e o sub-team {name} em modo limitado.",
                "Tente ajudar o usuario com base no seu conhecimento geral.",
                "Responda em portugues brasileiro.",
            ],
            markdown=True,
        )


def create_team() -> Team:
    """Cria o team principal no modo Route com 4 sub-teams especializados."""
    from app.agents.teams import (
        create_content_factory,
        create_analysis_squad,
        create_media_production,
        create_operations_team,
    )

    members = [
        _safe_create_sub_team(create_content_factory, "Content Factory"),
        _safe_create_sub_team(create_analysis_squad, "Analysis Squad"),
        _safe_create_sub_team(create_media_production, "Media Production"),
        _safe_create_sub_team(create_operations_team, "Operations"),
    ]

    team = Team(
        name="AgenteSocial Team",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        members=members,
        description="Time de IA especializado em gestao completa de redes sociais",
        instructions=[
            "Voce e o roteador principal do AgenteSocial, um ecossistema de IA para gestao de redes sociais.",
            "Analise a mensagem do usuario e ROTEIE para o sub-team MAIS adequado:",
            "",
            "ROTEAMENTO:",
            "- Criar posts, legendas, carrosseis, textos, design visual, hashtags → Content Factory",
            "- Analisar perfil, metricas, engajamento, tendencias, viral, estrategia → Analysis Squad",
            "- Podcast, roteiro de video, Reels, TikTok, YouTube, show notes → Media Production",
            "- Calendario editorial, relatorios, historico, preferencias, memoria → Operations",
            "",
            "REGRAS:",
            "1. Sempre roteie para exatamente 1 sub-team por mensagem.",
            "2. Se a mensagem envolver multiplas areas, priorize a principal.",
            "3. Responda SEMPRE em portugues brasileiro.",
        ],
        show_members_responses=True,
        enable_agentic_memory=True,
        markdown=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
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

        # Executa o team com session_id e user_id para persistencia nativa AGNO
        response = team.run(
            full_message,
            session_id=conversation_id,
            user_id=user_id,
        )
        response_text = response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        logger.error(f"Team execution error: {e}")
        response_text = "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente em alguns instantes."

    # Salva conversa no Supabase (non-blocking, fallback para quando AGNO storage nao esta ativo)
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
