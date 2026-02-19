from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from app.tools.memory_tools import get_memory_tools
from app.tools.supabase_tools import get_supabase_tools
from app.agents.memory_config import create_db, create_memory_manager


def create_memory_agent() -> Agent:
    return Agent(
        name="Memory Agent",
        model=OpenAIResponses(id="gpt-4.1-nano"),
        role="Agente de memoria e contexto",
        description="Gerencia memoria de longo prazo, brand voice, historico de conteudo e aprendizados. Use para buscar contexto, salvar preferencias e manter consistencia.",
        instructions=[
            "Voce gerencia a memoria de longo prazo do sistema.",
            "3 camadas de memoria:",
            "  1. Working Memory: sessao atual (contexto imediato)",
            "  2. Episodic Memory: historico recente, 90 dias (PostgreSQL)",
            "  3. Semantic Memory: conhecimento permanente (pgvector RAG)",
            "Armazene e recupere: brand voice, preferencias, historico, aprendizados.",
            "Mantenha consistencia de estilo e tom ao longo do tempo.",
            "Detecte padroes de sucesso em conteudos anteriores.",
            "Responda em portugues brasileiro.",
        ],
        tools=[*get_memory_tools(), *get_supabase_tools()],
        markdown=True,
        store_history_messages=True,
        add_history_to_context=True,
        num_history_runs=5,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
