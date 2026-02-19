from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from app.agents.memory_config import create_db, create_memory_manager


def create_master_agent() -> Agent:
    return Agent(
        name="Master Orchestrator",
        model=OpenAIResponses(id="gpt-4.1-mini"),
        role="Orquestrador principal do AgenteSocial",
        description="Coordena todos os agentes e decide qual especialista deve responder",
        instructions=[
            "Voce e o orquestrador do AgenteSocial, um ecossistema de IA para gestao de redes sociais.",
            "Analise cada mensagem e delegue para o agente MAIS adequado:",
            "",
            "ROUTING:",
            "- Criar posts, legendas, textos → Content Writer",
            "- Analisar perfil, metricas, engajamento → Social Media Analyst",
            "- Tendencias, conteudo viral → Viral Content Tracker",
            "- Hashtags, descoberta → Hashtag Hunter",
            "- Roteiro podcast, show notes → Podcast Creator",
            "- Roteiro video, Reels, Shorts → Video Script Writer",
            "- Calendario, planejamento editorial → Calendar Planner",
            "- Relatorios, performance → Report Generator",
            "- Estrategia, crescimento → Strategy Advisor",
            "- Design, visual, layout → Visual Designer",
            "- Historico, contexto, preferencias → Memory Agent",
            "",
            "REGRAS:",
            "1. SEMPRE consulte o Memory Agent antes de delegar para contexto do usuario.",
            "2. Se a tarefa envolver multiplos agentes, coordene a execucao sequencial.",
            "3. Se nenhum agente especialista for adequado, responda voce mesmo.",
            "4. Responda SEMPRE em portugues brasileiro.",
            "5. Seja conciso e acionavel nas respostas.",
        ],
        markdown=True,
        store_history_messages=True,
        add_history_to_context=True,
        num_history_runs=5,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
