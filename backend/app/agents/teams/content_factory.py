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
            "NUNCA pergunte 'quer que eu comece?' ou 'por onde prefere comecar?'. "
            "EXECUTE imediatamente delegando aos membros e compilando a resposta final.",
            "",
            "FLUXO OBRIGATORIO (execute em sequencia, sem perguntar):",
            "1. Delegue ao Content Writer: 'Crie IMEDIATAMENTE [o conteudo pedido]. NAO faca perguntas.'",
            "2. Delegue ao Visual Designer: 'Crie IMEDIATAMENTE sugestoes visuais para [o conteudo]. NAO faca perguntas.'",
            "3. Delegue ao Hashtag Hunter: 'Pesquise e gere IMEDIATAMENTE hashtags para [o tema]. NAO faca perguntas.'",
            "4. Compile TUDO em uma resposta unica, organizada e completa.",
            "",
            "Se um membro retornar uma pergunta em vez de conteudo, IGNORE a pergunta e use o que foi gerado. "
            "Se um membro falhar, continue com os outros e entregue o que tiver.",
            "",
            "Para pedidos de PLANO COMPLETO ou PACOTE DE CONTEUDO:",
            "- Delegue ao Content Writer para gerar TODO o conteudo (posts, stories, reels, frases, calendario).",
            "- O Content Writer deve gerar o maximo possivel em uma unica resposta.",
            "- Visual Designer complementa com sugestoes visuais.",
            "- Hashtag Hunter complementa com estrategia de hashtags.",
            "",
            "Responda SEMPRE em portugues brasileiro.",
        ],
        markdown=True,
        show_members_responses=True,
        enable_agentic_memory=True,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
