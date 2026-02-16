from agno.tools import tool
from app.constants import TABLES


@tool
def query_table(table_name: str, filters: dict = None, select: str = "*", limit: int = 50) -> str:
    """Consulta generica em tabelas do Supabase."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    allowed_tables = list(TABLES.values())
    if table_name not in allowed_tables:
        return f"Tabela '{table_name}' nao permitida. Tabelas disponiveis: {allowed_tables}"

    try:
        query = supabase.table(table_name).select(select)
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.limit(limit).execute()
        return str(result.data) if result.data else "Nenhum resultado encontrado."
    except Exception as e:
        return f"Erro na consulta: {e}"


@tool
def insert_record(table_name: str, data: dict) -> str:
    """Insere registro em uma tabela do Supabase."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    writable_tables = [
        TABLES["content_pieces"], TABLES["content_calendar"], TABLES["viral_content"],
        TABLES["hashtag_research"], TABLES["podcast_episodes"], TABLES["reports"],
        TABLES["analytics_snapshots"], TABLES["notifications"], TABLES["content_history"],
        TABLES["brand_voice_profiles"], TABLES["competitor_tracking"],
    ]
    if table_name not in writable_tables:
        return f"Tabela '{table_name}' nao permitida para insercao."

    try:
        result = supabase.table(table_name).insert(data).execute()
        return f"Registro inserido: {result.data[0]['id']}" if result.data else "Erro ao inserir."
    except Exception as e:
        return f"Erro ao inserir: {e}"


def get_supabase_tools():
    return [query_table, insert_record]
