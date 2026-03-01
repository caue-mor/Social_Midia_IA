"""Toolkit de pesquisa unificado — Tavily + Newspaper4k com fallback DuckDuckGo."""

import json
from agno.tools import tool


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Pesquisa na web com citacoes e fontes. Usa Tavily (com fallback DuckDuckGo)."""
    # Tenta Tavily primeiro
    try:
        try:
            from app.config import get_settings
            api_key = get_settings().TAVILY_API_KEY
        except Exception:
            import os
            api_key = os.getenv("TAVILY_API_KEY", "")
        if api_key:
            from tavily import TavilyClient
            client = TavilyClient(api_key=api_key)
            response = client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",
                include_answer=True,
            )
            results = []
            for r in response.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:500],
                    "score": r.get("score", 0),
                })
            return json.dumps({
                "source": "tavily",
                "answer": response.get("answer", ""),
                "results": results,
            }, ensure_ascii=False)
    except ImportError:
        pass
    except Exception as e:
        # Tavily falhou, tenta fallback
        pass

    # Fallback: DuckDuckGo (tenta ddgs primeiro, depois duckduckgo_search)
    for ddgs_module in ["ddgs", "duckduckgo_search"]:
        try:
            DDGS = __import__(ddgs_module, fromlist=["DDGS"]).DDGS
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "content": r.get("body", "")[:500],
                    })
                return json.dumps({
                    "source": "duckduckgo",
                    "answer": "",
                    "results": results,
                }, ensure_ascii=False)
        except Exception:
            continue

    return "Nenhum provedor de pesquisa disponivel. Configure TAVILY_API_KEY ou instale ddgs."


@tool
def extract_article(url: str) -> str:
    """Extrai conteudo completo de um artigo/noticia (titulo, texto, autores, data). Usa Newspaper4k."""
    # Tenta Newspaper4k
    try:
        from newspaper import Article

        article = Article(url, language="pt")
        article.download()
        article.parse()

        result = {
            "source": "newspaper4k",
            "title": article.title or "",
            "authors": article.authors or [],
            "publish_date": str(article.publish_date) if article.publish_date else "",
            "text": article.text[:3000] if article.text else "",
            "top_image": article.top_image or "",
            "keywords": list(article.keywords)[:10] if article.keywords else [],
        }

        # Tenta NLP para keywords extras
        try:
            article.nlp()
            result["summary"] = article.summary[:500] if article.summary else ""
            result["nlp_keywords"] = list(article.keywords)[:10] if article.keywords else []
        except Exception:
            pass

        return json.dumps(result, ensure_ascii=False)
    except ImportError:
        return (
            "newspaper4k nao instalado. Execute: uv pip install newspaper4k lxml_html_clean\n"
            "Dica: use web_search() como alternativa para pesquisar conteudo."
        )
    except Exception as e:
        return f"Erro ao extrair artigo de {url}: {e}"


@tool
def search_trending_content(topic: str, platform: str = "geral") -> str:
    """Pesquisa conteudo trending combinando pesquisa web + Google Trends. Plataformas: instagram, tiktok, youtube, linkedin, geral."""
    results = {"topic": topic, "platform": platform, "web_results": [], "trends": {}}

    # Pesquisa web direcionada
    platform_queries = {
        "instagram": f"{topic} trending Instagram 2026 Brasil",
        "tiktok": f"{topic} viral TikTok tendencia Brasil",
        "youtube": f"{topic} trending YouTube Brasil mais vistos",
        "linkedin": f"{topic} trending LinkedIn posts virais",
        "geral": f"{topic} tendencia redes sociais Brasil 2026",
    }
    query = platform_queries.get(platform, platform_queries["geral"])

    try:
        web_data = web_search(query, max_results=5)
        if isinstance(web_data, str):
            web_parsed = json.loads(web_data)
            results["web_results"] = web_parsed.get("results", [])
    except Exception:
        pass

    # Google Trends
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="pt-BR", tz=180)
        keywords = [topic]
        if platform != "geral":
            keywords.append(f"{topic} {platform}")

        pytrends.build_payload(keywords[:5], cat=0, timeframe="today 1-m", geo="BR")
        interest = pytrends.interest_over_time()

        if not interest.empty:
            for kw in keywords:
                if kw in interest.columns:
                    values = interest[kw].values
                    results["trends"][kw] = {
                        "current_interest": int(values[-1]),
                        "direction": "up" if len(values) >= 2 and int(values[-1]) > int(values[0]) + 5 else
                                     "down" if len(values) >= 2 and int(values[-1]) < int(values[0]) - 5 else "stable",
                    }

        # Related queries
        related = pytrends.related_queries()
        related_list = []
        if topic in related:
            rising = related[topic].get("rising")
            if rising is not None and not rising.empty:
                related_list = rising.head(5).to_dict("records")
        results["related_queries"] = related_list
    except Exception:
        results["trends"] = {"note": "Google Trends indisponivel"}

    return json.dumps(results, ensure_ascii=False)


@tool
def analyze_competitor_page(url: str) -> str:
    """Analisa pagina publica de concorrente via scraping. Extrai bio, posts recentes, metricas publicas."""
    # Tenta Crawl4ai
    try:
        import asyncio
        from crawl4ai import AsyncWebCrawler

        async def _scrape():
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                return result.markdown[:5000] if result.markdown else ""

        # Roda async em sync
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    content = pool.submit(asyncio.run, _scrape()).result(timeout=30)
            else:
                content = loop.run_until_complete(_scrape())
        except RuntimeError:
            content = asyncio.run(_scrape())

        return json.dumps({
            "source": "crawl4ai",
            "url": url,
            "content": content,
            "note": "Analise o conteudo acima para extrair insights sobre o concorrente.",
        }, ensure_ascii=False)
    except ImportError:
        pass

    # Fallback: pesquisa web sobre o perfil
    try:
        search_query = f"site:{url} OR {url} perfil analise"
        web_data = web_search(search_query, max_results=3)
        return json.dumps({
            "source": "web_search_fallback",
            "url": url,
            "note": "crawl4ai nao instalado. Usando pesquisa web como fallback.",
            "web_results": json.loads(web_data) if isinstance(web_data, str) else {},
        }, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao analisar pagina do concorrente: {e}"


def get_research_tools() -> list:
    """Retorna ferramentas de pesquisa disponiveis (degrada gracefully)."""
    return [
        web_search,
        extract_article,
        search_trending_content,
        analyze_competitor_page,
    ]
