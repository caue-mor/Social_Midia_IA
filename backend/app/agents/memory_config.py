"""
Configuracao centralizada de PostgresDb e MemoryManager para AGNO 2.5.2.

Degradacao graciosa: retorna None se DATABASE_URL nao estiver configurado.

Uso em agentes:
    from app.agents.memory_config import create_db, create_memory_manager

    Agent(
        ...,
        db=create_db(),
        memory_manager=create_memory_manager(),
    )
"""

import logging
from typing import Optional

logger = logging.getLogger("agentesocial.memory_config")


def _get_database_url() -> str:
    """Obtem DATABASE_URL das settings."""
    try:
        from app.config import get_settings
        return get_settings().DATABASE_URL
    except Exception:
        return ""


def create_db(
    session_table: str = "agno_sessions",
    memory_table: str = "agno_memories",
) -> Optional["PostgresDb"]:
    """Cria PostgresDb para storage de sessoes e memoria.

    AGNO 2.5.2 auto-cria tabelas no schema 'ai' com create_schema=True (default).
    Tabelas padrao: ai.agno_sessions, ai.agno_memories, etc.

    Args:
        session_table: Tabela para sessoes de agente/team.
        memory_table: Tabela para memorias.
    """
    db_url = _get_database_url()
    if not db_url:
        logger.info("DATABASE_URL nao configurado — agentes rodarao sem persistencia")
        return None

    try:
        from agno.db.postgres import PostgresDb

        return PostgresDb(
            db_url=db_url,
            session_table=session_table,
            memory_table=memory_table,
        )
    except Exception as e:
        logger.warning(f"Falha ao criar PostgresDb: {e}")
        return None


def create_memory_manager() -> Optional["MemoryManager"]:
    """Cria MemoryManager com PostgresDb para memoria agentesocial.

    Retorna None se DATABASE_URL nao estiver configurado.
    """
    db = create_db()
    if db is None:
        return None

    try:
        from agno.memory.manager import MemoryManager

        return MemoryManager(db=db)
    except Exception as e:
        logger.warning(f"Falha ao criar MemoryManager: {e}")
        return None
