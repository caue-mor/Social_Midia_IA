import httpx
from agno.tools import tool
from app.services.token_manager import get_user_instagram_credentials

GRAPH_API_BASE = "https://graph.instagram.com/v25.0"

_INSTAGRAM_NOT_CONFIGURED_MSG = (
    "A integracao com o Instagram ainda nao esta configurada. "
    "Para conectar sua conta, acesse Configuracoes > Integracoes > Instagram "
    "e clique em 'Conectar Instagram' para autorizar via OAuth. "
    "Enquanto isso, voce pode usar a ferramenta get_instagram_mock_data() "
    "para ver uma demonstracao com dados de exemplo."
)


@tool
def get_instagram_profile(handle: str, user_id: str = "") -> str:
    """Busca informacoes do perfil Instagram via Graph API."""
    creds = get_user_instagram_credentials(user_id)
    if not creds:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds
    url = f"{GRAPH_API_BASE}/me"
    params = {
        "fields": "user_id,username,name,biography,followers_count,follows_count,media_count,profile_picture_url",
        "access_token": access_token,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao buscar perfil: {e}"


@tool
def get_instagram_media(limit: int = 25, user_id: str = "") -> str:
    """Busca posts recentes do Instagram via Graph API."""
    creds = get_user_instagram_credentials(user_id)
    if not creds:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds
    url = f"{GRAPH_API_BASE}/me/media"
    params = {
        "fields": "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count",
        "limit": min(limit, 100),
        "access_token": access_token,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao buscar media: {e}"


@tool
def get_instagram_insights(media_id: str, user_id: str = "") -> str:
    """Busca insights de um post especifico do Instagram."""
    creds = get_user_instagram_credentials(user_id)
    if not creds:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds
    url = f"{GRAPH_API_BASE}/{media_id}/insights"
    params = {
        "metric": "engagement,impressions,reach,saved,shares",
        "access_token": access_token,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao buscar insights: {e}"


@tool
def search_instagram_hashtag(hashtag: str, user_id: str = "") -> str:
    """Pesquisa uma hashtag no Instagram e retorna volume."""
    creds = get_user_instagram_credentials(user_id)
    if not creds:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds

    # Hashtag search uses graph.facebook.com (requires IG user ID)
    url = "https://graph.facebook.com/v25.0/ig_hashtag_search"
    params = {
        "q": hashtag.replace("#", ""),
        "user_id": account_id,
        "access_token": access_token,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("data"):
            hashtag_id = data["data"][0]["id"]
            media_url = f"https://graph.facebook.com/v25.0/{hashtag_id}/top_media"
            media_params = {
                "user_id": account_id,
                "fields": "id,caption,media_type,like_count,comments_count,permalink",
                "access_token": access_token,
            }
            media_resp = httpx.get(media_url, params=media_params, timeout=30)
            media_resp.raise_for_status()
            return str(media_resp.json())
        return "Hashtag nao encontrada."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return (
                "A pesquisa de hashtags pode nao estar disponivel com Instagram Login. "
                "Este recurso requer permissoes especificas do app Meta."
            )
        return f"Erro ao pesquisar hashtag: {e}"
    except Exception as e:
        return f"Erro ao pesquisar hashtag: {e}"


@tool
def get_instagram_mock_data() -> str:
    """Retorna dados de demonstracao do Instagram para quando a API nao esta configurada. Use para mostrar as capacidades de analise com dados de exemplo."""
    return str({
        "_aviso": "DADOS DE DEMONSTRACAO - Nao sao dados reais. Configure a API do Instagram para dados reais.",
        "profile": {
            "username": "marca_exemplo",
            "name": "Marca Exemplo",
            "biography": "Transformando ideias em resultados | Marketing Digital",
            "followers_count": 45200,
            "follows_count": 1230,
            "media_count": 487,
        },
        "recent_posts": [
            {
                "id": "demo_001",
                "caption": "5 dicas para aumentar seu engajamento no Instagram",
                "media_type": "CAROUSEL_ALBUM",
                "like_count": 1820,
                "comments_count": 145,
                "shares": 320,
                "saves": 890,
                "reach": 28500,
                "impressions": 42000,
                "timestamp": "2026-02-13T10:30:00Z",
            },
            {
                "id": "demo_002",
                "caption": "Bastidores do nosso processo criativo",
                "media_type": "VIDEO",
                "like_count": 2340,
                "comments_count": 198,
                "shares": 156,
                "saves": 412,
                "reach": 35200,
                "impressions": 51000,
                "timestamp": "2026-02-11T14:00:00Z",
            },
            {
                "id": "demo_003",
                "caption": "Novo produto disponivel! Link na bio",
                "media_type": "IMAGE",
                "like_count": 890,
                "comments_count": 67,
                "shares": 45,
                "saves": 123,
                "reach": 18700,
                "impressions": 25000,
                "timestamp": "2026-02-09T09:00:00Z",
            },
            {
                "id": "demo_004",
                "caption": "Tutorial: Como criar Reels que viralizam",
                "media_type": "VIDEO",
                "like_count": 3100,
                "comments_count": 276,
                "shares": 520,
                "saves": 1450,
                "reach": 62000,
                "impressions": 89000,
                "timestamp": "2026-02-07T16:30:00Z",
            },
            {
                "id": "demo_005",
                "caption": "Depoimento de cliente satisfeito",
                "media_type": "CAROUSEL_ALBUM",
                "like_count": 1560,
                "comments_count": 89,
                "shares": 210,
                "saves": 345,
                "reach": 22400,
                "impressions": 31000,
                "timestamp": "2026-02-05T11:00:00Z",
            },
        ],
        "metrics_summary": {
            "avg_engagement_rate": 4.2,
            "avg_reach": 33360,
            "avg_impressions": 47600,
            "best_content_type": "VIDEO",
            "best_posting_time": "16:00-17:00",
            "best_posting_day": "terca-feira",
            "follower_growth_weekly": 1.8,
            "posts_per_week": 3.5,
        },
        "top_hashtags": [
            {"tag": "#marketingdigital", "posts_count": 42, "avg_reach": 28000},
            {"tag": "#dicasdemarketing", "posts_count": 35, "avg_reach": 31000},
            {"tag": "#empreendedorismo", "posts_count": 28, "avg_reach": 24000},
            {"tag": "#socialmedia", "posts_count": 22, "avg_reach": 19000},
            {"tag": "#crescimentoorganico", "posts_count": 15, "avg_reach": 35000},
        ],
    })


def get_instagram_tools():
    return [
        get_instagram_profile,
        get_instagram_media,
        get_instagram_insights,
        search_instagram_hashtag,
        get_instagram_mock_data,
    ]
