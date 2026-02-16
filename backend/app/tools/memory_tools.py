from agno.tools import tool
from app.constants import TABLES


@tool
def search_content_memory(query: str, user_id: str, limit: int = 10) -> str:
    """Busca na memoria semantica (pgvector) por conteudo similar."""
    try:
        from app.services.embedding_service import get_embedding
        from app.database.supabase_client import get_supabase

        # Try semantic search with embeddings
        embedding = get_embedding(query)
        supabase = get_supabase()
        result = supabase.rpc("match_content_by_embedding", {
            "query_embedding": embedding,
            "match_count": limit,
            "filter_user_id": user_id,
            "similarity_threshold": 0.7,
        }).execute()

        if result.data:
            return str(result.data)
    except Exception:
        pass

    # Fallback to text search
    try:
        from app.database.supabase_client import get_supabase
        supabase = get_supabase()
        result = supabase.rpc("match_content", {
            "query_text": query,
            "match_count": limit,
            "filter_user_id": user_id,
        }).execute()
        return str(result.data) if result.data else "Nenhum conteudo encontrado na memoria."
    except Exception as e:
        return f"Erro ao buscar memoria: {e}"


@tool
def save_to_memory(user_id: str, content: str, content_type: str, metadata: dict = None) -> str:
    """Salva conteudo na memoria episodica com embedding vetorial."""
    try:
        from app.services.embedding_service import get_embedding
        from app.database.supabase_client import get_supabase

        embedding = get_embedding(content)
        supabase = get_supabase()
        data = {
            "user_id": user_id,
            "content": content,
            "content_type": content_type,
            "embedding": embedding,
            "metadata": metadata or {},
        }
        result = supabase.table(TABLES["content_history"]).insert(data).execute()
        return f"Salvo na memoria: {result.data[0]['id']}" if result.data else "Erro ao salvar."
    except Exception:
        # Fallback without embedding
        try:
            from app.database.supabase_client import get_supabase
            supabase = get_supabase()
            data = {
                "user_id": user_id,
                "content": content,
                "content_type": content_type,
                "metadata": metadata or {},
            }
            result = supabase.table(TABLES["content_history"]).insert(data).execute()
            return f"Salvo na memoria (sem embedding): {result.data[0]['id']}" if result.data else "Erro ao salvar."
        except Exception as e:
            return f"Erro ao salvar na memoria: {e}"


@tool
def get_brand_voice(user_id: str) -> str:
    """Busca o brand voice (tom de voz da marca) do usuario."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    try:
        result = supabase.table(TABLES["brand_voice_profiles"]).select("*").eq("user_id", user_id).eq("is_active", True).maybe_single().execute()
        if result.data:
            return str(result.data)
        return "Brand voice nao configurado para este usuario."
    except Exception as e:
        return f"Erro ao buscar brand voice: {e}"


@tool
def get_content_history(user_id: str, platform: str = None, limit: int = 20) -> str:
    """Busca historico de conteudo gerado pelo usuario."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    try:
        query = supabase.table(TABLES["content_pieces"]).select("*").eq("user_id", user_id)
        if platform:
            query = query.eq("platform", platform)
        result = query.order("created_at", desc=True).limit(limit).execute()
        return str(result.data) if result.data else "Nenhum conteudo encontrado."
    except Exception as e:
        return f"Erro ao buscar historico: {e}"


@tool
def get_competitor_data(user_id: str) -> str:
    """Busca dados de concorrentes rastreados pelo usuario."""
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()

    try:
        result = supabase.table(TABLES["competitor_tracking"]).select("*").eq("user_id", user_id).execute()
        return str(result.data) if result.data else "Nenhum concorrente rastreado."
    except Exception as e:
        return f"Erro ao buscar concorrentes: {e}"


def get_memory_tools():
    return [search_content_memory, save_to_memory, get_brand_voice, get_content_history, get_competitor_data]
