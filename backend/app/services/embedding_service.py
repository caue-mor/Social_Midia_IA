import logging
from openai import OpenAI
from app.config import get_settings

logger = logging.getLogger("agentesocial.embedding")

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


def get_embedding(text: str) -> list[float]:
    """Generate embedding for text using OpenAI."""
    settings = get_settings()
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not configured")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Truncate to ~8000 tokens (~32000 chars)
    truncated = text[:32000]

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=truncated,
    )
    return response.data[0].embedding


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for multiple texts in a single API call."""
    settings = get_settings()
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    truncated = [t[:32000] for t in texts]

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=truncated,
    )
    return [item.embedding for item in response.data]


async def save_with_embedding(
    user_id: str,
    content: str,
    content_type: str,
    metadata: dict = None,
) -> str:
    """Save content to memory with embedding vector."""
    from app.database.supabase_client import get_supabase
    from app.constants import TABLES

    try:
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
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        logger.error(f"Failed to save with embedding: {e}")
        # Fallback: save without embedding
        from app.database.supabase_client import get_supabase
        supabase = get_supabase()
        data = {
            "user_id": user_id,
            "content": content,
            "content_type": content_type,
            "metadata": metadata or {},
        }
        result = supabase.table(TABLES["content_history"]).insert(data).execute()
        return result.data[0]["id"] if result.data else None


async def semantic_search(
    query: str,
    user_id: str,
    limit: int = 10,
    threshold: float = 0.7,
) -> list[dict]:
    """Search content by semantic similarity using embeddings."""
    from app.database.supabase_client import get_supabase

    try:
        embedding = get_embedding(query)

        supabase = get_supabase()
        result = supabase.rpc("match_content_by_embedding", {
            "query_embedding": embedding,
            "match_count": limit,
            "filter_user_id": user_id,
            "similarity_threshold": threshold,
        }).execute()

        return result.data or []
    except Exception as e:
        logger.warning(f"Semantic search failed, falling back to text: {e}")
        # Fallback to text search
        supabase = get_supabase()
        result = supabase.rpc("match_content", {
            "query_text": query,
            "match_count": limit,
            "filter_user_id": user_id,
        }).execute()
        return result.data or []
