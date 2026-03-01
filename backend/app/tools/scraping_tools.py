"""Scrapers especializados para redes sociais publicas via Crawl4ai."""

import json
from agno.tools import tool

CRAWL4AI_NOT_INSTALLED = (
    "crawl4ai nao instalado. Execute: uv pip install crawl4ai\n"
    "Dica: use web_search() como alternativa para pesquisar dados publicos."
)


def _run_async_scrape(url: str, timeout: int = 30) -> str:
    """Helper para rodar scrape async em contexto sync."""
    import asyncio
    from crawl4ai import AsyncWebCrawler

    async def _scrape():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown[:5000] if result.markdown else ""

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, _scrape()).result(timeout=timeout)
        else:
            return loop.run_until_complete(_scrape())
    except RuntimeError:
        return asyncio.run(_scrape())


@tool
def scrape_public_page(url: str) -> str:
    """Scrape pagina publica (Instagram, TikTok, blog, etc) e retorna conteudo em markdown."""
    try:
        from crawl4ai import AsyncWebCrawler  # noqa: F401 — verifica instalacao
    except ImportError:
        return CRAWL4AI_NOT_INSTALLED

    try:
        content = _run_async_scrape(url)
        return json.dumps({
            "source": "crawl4ai",
            "url": url,
            "content": content,
        }, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao fazer scrape de {url}: {e}"


@tool
def scrape_instagram_profile(username: str) -> str:
    """Scrape pagina publica de um perfil Instagram. Extrai bio, posts recentes e dados publicos. NAO precisa de API key."""
    try:
        from crawl4ai import AsyncWebCrawler  # noqa: F401
    except ImportError:
        # Fallback: pesquisa web
        try:
            from app.tools.research_tools import web_search
            result = web_search(f"instagram.com/{username} perfil bio seguidores", max_results=3)
            return json.dumps({
                "source": "web_search_fallback",
                "username": username,
                "note": "crawl4ai nao instalado. Dados obtidos via pesquisa web.",
                "web_results": json.loads(result) if isinstance(result, str) else {},
            }, ensure_ascii=False)
        except Exception:
            return CRAWL4AI_NOT_INSTALLED

    try:
        url = f"https://www.instagram.com/{username}/"
        content = _run_async_scrape(url)
        return json.dumps({
            "source": "crawl4ai",
            "username": username,
            "url": url,
            "content": content,
            "note": "Analise o conteudo para extrair: bio, contagem de seguidores, posts recentes, temas.",
        }, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao scrape do perfil @{username}: {e}"


@tool
def scrape_tiktok_trending(keyword: str) -> str:
    """Busca conteudo trending no TikTok para um keyword via web scraping."""
    try:
        from crawl4ai import AsyncWebCrawler  # noqa: F401
    except ImportError:
        # Fallback: pesquisa web
        try:
            from app.tools.research_tools import web_search
            result = web_search(f"{keyword} trending TikTok viral Brasil 2026", max_results=5)
            return json.dumps({
                "source": "web_search_fallback",
                "keyword": keyword,
                "platform": "tiktok",
                "note": "crawl4ai nao instalado. Dados obtidos via pesquisa web.",
                "web_results": json.loads(result) if isinstance(result, str) else {},
            }, ensure_ascii=False)
        except Exception:
            return CRAWL4AI_NOT_INSTALLED

    try:
        url = f"https://www.tiktok.com/search?q={keyword}"
        content = _run_async_scrape(url)
        return json.dumps({
            "source": "crawl4ai",
            "keyword": keyword,
            "platform": "tiktok",
            "url": url,
            "content": content,
            "note": "Analise o conteudo para identificar videos virais, hashtags e tendencias.",
        }, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao buscar trending TikTok para '{keyword}': {e}"


@tool
def scrape_youtube_trending(topic: str) -> str:
    """Busca videos trending no YouTube para um topico via web scraping."""
    try:
        from crawl4ai import AsyncWebCrawler  # noqa: F401
    except ImportError:
        # Fallback: pesquisa web
        try:
            from app.tools.research_tools import web_search
            result = web_search(f"{topic} YouTube trending videos Brasil mais vistos", max_results=5)
            return json.dumps({
                "source": "web_search_fallback",
                "topic": topic,
                "platform": "youtube",
                "note": "crawl4ai nao instalado. Dados obtidos via pesquisa web.",
                "web_results": json.loads(result) if isinstance(result, str) else {},
            }, ensure_ascii=False)
        except Exception:
            return CRAWL4AI_NOT_INSTALLED

    try:
        url = f"https://www.youtube.com/results?search_query={topic}&sp=CAMSAhAB"
        content = _run_async_scrape(url)
        return json.dumps({
            "source": "crawl4ai",
            "topic": topic,
            "platform": "youtube",
            "url": url,
            "content": content,
            "note": "Analise o conteudo para identificar videos populares, titulos e tendencias.",
        }, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao buscar trending YouTube para '{topic}': {e}"


def get_scraping_tools() -> list:
    """Retorna ferramentas de scraping disponiveis (degrada gracefully)."""
    return [
        scrape_public_page,
        scrape_instagram_profile,
        scrape_tiktok_trending,
        scrape_youtube_trending,
    ]
