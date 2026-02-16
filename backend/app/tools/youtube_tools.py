import httpx
from agno.tools import tool
from app.config import get_settings

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

_YOUTUBE_NOT_CONFIGURED_MSG = (
    "A integracao com o YouTube ainda nao esta configurada. "
    "Para conectar, acesse Configuracoes > Integracoes > YouTube "
    "e adicione sua YOUTUBE_API_KEY (obtenha em console.cloud.google.com). "
    "Enquanto isso, voce pode usar a ferramenta get_youtube_mock_data() "
    "para ver uma demonstracao com dados de exemplo."
)


@tool
def get_youtube_channel(channel_id: str) -> str:
    """Busca informacoes de um canal do YouTube."""
    settings = get_settings()
    if not settings.YOUTUBE_API_KEY:
        return _YOUTUBE_NOT_CONFIGURED_MSG

    url = f"{YOUTUBE_API_BASE}/channels"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": channel_id,
        "key": settings.YOUTUBE_API_KEY,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao buscar canal: {e}"


@tool
def search_youtube_videos(query: str, max_results: int = 10) -> str:
    """Pesquisa videos no YouTube por palavra-chave."""
    settings = get_settings()
    if not settings.YOUTUBE_API_KEY:
        return _YOUTUBE_NOT_CONFIGURED_MSG

    url = f"{YOUTUBE_API_BASE}/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "viewCount",
        "maxResults": min(max_results, 50),
        "key": settings.YOUTUBE_API_KEY,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao pesquisar videos: {e}"


@tool
def get_youtube_video_stats(video_id: str) -> str:
    """Busca estatisticas de um video do YouTube."""
    settings = get_settings()
    if not settings.YOUTUBE_API_KEY:
        return _YOUTUBE_NOT_CONFIGURED_MSG

    url = f"{YOUTUBE_API_BASE}/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": video_id,
        "key": settings.YOUTUBE_API_KEY,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao buscar video: {e}"


@tool
def get_youtube_trending(region_code: str = "BR", category_id: str = "0") -> str:
    """Busca videos em alta no YouTube por regiao."""
    settings = get_settings()
    if not settings.YOUTUBE_API_KEY:
        return _YOUTUBE_NOT_CONFIGURED_MSG

    url = f"{YOUTUBE_API_BASE}/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "videoCategoryId": category_id,
        "maxResults": 20,
        "key": settings.YOUTUBE_API_KEY,
    }
    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return str(resp.json())
    except Exception as e:
        return f"Erro ao buscar trending: {e}"


@tool
def get_youtube_mock_data() -> str:
    """Retorna dados de demonstracao do YouTube para quando a API nao esta configurada. Use para mostrar as capacidades de analise com dados de exemplo."""
    return str({
        "_aviso": "DADOS DE DEMONSTRACAO - Nao sao dados reais. Configure a API do YouTube para dados reais.",
        "channel": {
            "id": "UC_demo_channel",
            "title": "Canal Exemplo Digital",
            "description": "Dicas de marketing digital e empreendedorismo",
            "subscriber_count": 128000,
            "video_count": 342,
            "view_count": 18500000,
            "created_at": "2022-03-15T00:00:00Z",
        },
        "recent_videos": [
            {
                "id": "demo_vid_001",
                "title": "Como Criar Conteudo que Viraliza em 2026",
                "published_at": "2026-02-12T14:00:00Z",
                "view_count": 45200,
                "like_count": 3200,
                "comment_count": 287,
                "duration": "PT12M34S",
                "tags": ["marketing digital", "viralizacao", "conteudo"],
            },
            {
                "id": "demo_vid_002",
                "title": "5 Ferramentas de IA para Social Media",
                "published_at": "2026-02-08T14:00:00Z",
                "view_count": 89300,
                "like_count": 6100,
                "comment_count": 543,
                "duration": "PT18M22S",
                "tags": ["ia", "ferramentas", "social media"],
            },
            {
                "id": "demo_vid_003",
                "title": "Estrategia Completa para Instagram em 2026",
                "published_at": "2026-02-05T14:00:00Z",
                "view_count": 62100,
                "like_count": 4500,
                "comment_count": 398,
                "duration": "PT22M10S",
                "tags": ["instagram", "estrategia", "2026"],
            },
            {
                "id": "demo_vid_004",
                "title": "Como Monetizar seu Canal do YouTube",
                "published_at": "2026-02-01T14:00:00Z",
                "view_count": 135000,
                "like_count": 9800,
                "comment_count": 876,
                "duration": "PT25M45S",
                "tags": ["monetizacao", "youtube", "renda"],
            },
        ],
        "metrics_summary": {
            "avg_views_per_video": 82900,
            "avg_like_rate": 6.8,
            "avg_comment_rate": 0.8,
            "subscriber_growth_monthly": 3.2,
            "best_video_length": "15-25 min",
            "best_publishing_day": "terca-feira",
            "best_publishing_time": "14:00",
            "top_performing_tags": ["ia", "ferramentas", "monetizacao"],
            "avg_ctr": 8.5,
            "avg_retention": 42.0,
        },
    })


def get_youtube_tools():
    return [
        get_youtube_channel,
        search_youtube_videos,
        get_youtube_video_stats,
        get_youtube_trending,
        get_youtube_mock_data,
    ]
