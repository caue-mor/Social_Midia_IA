from agno.tools import tool


@tool
def get_google_trends(keywords: list[str], timeframe: str = "today 3-m", geo: str = "BR") -> str:
    """Busca tendencias no Google Trends para as keywords fornecidas."""
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="pt-BR", tz=180)
        pytrends.build_payload(keywords[:5], cat=0, timeframe=timeframe, geo=geo)

        # Interest over time
        interest = pytrends.interest_over_time()
        if interest.empty:
            return f"Sem dados de tendencia para: {keywords}"

        result = {
            "keywords": keywords,
            "timeframe": timeframe,
            "geo": geo,
            "latest_values": {},
            "trend_direction": {},
        }

        for kw in keywords:
            if kw in interest.columns:
                values = interest[kw].values
                result["latest_values"][kw] = int(values[-1])
                if len(values) >= 2:
                    diff = int(values[-1]) - int(values[0])
                    result["trend_direction"][kw] = "up" if diff > 5 else "down" if diff < -5 else "stable"

        return str(result)
    except ImportError:
        return "pytrends nao instalado. Execute: pip install pytrends"
    except Exception as e:
        return f"Erro ao buscar trends: {e}"


@tool
def get_related_queries(keyword: str, geo: str = "BR") -> str:
    """Busca queries relacionadas a uma keyword no Google Trends."""
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="pt-BR", tz=180)
        pytrends.build_payload([keyword], cat=0, timeframe="today 3-m", geo=geo)

        related = pytrends.related_queries()
        result = {"keyword": keyword, "top": [], "rising": []}

        if keyword in related:
            top = related[keyword].get("top")
            rising = related[keyword].get("rising")
            if top is not None and not top.empty:
                result["top"] = top.head(10).to_dict("records")
            if rising is not None and not rising.empty:
                result["rising"] = rising.head(10).to_dict("records")

        return str(result)
    except Exception as e:
        return f"Erro ao buscar queries relacionadas: {e}"


@tool
def get_trending_searches(country: str = "brazil") -> str:
    """Busca pesquisas em alta no Google do pais especificado."""
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="pt-BR", tz=180)
        trending = pytrends.trending_searches(pn=country)
        return str(trending.head(20).values.tolist())
    except Exception as e:
        return f"Erro ao buscar trending searches: {e}"


@tool
def get_interest_by_region(keyword: str, geo: str = "BR") -> str:
    """Busca interesse regional por uma keyword no Google Trends. Mostra em quais regioes/estados o interesse e maior."""
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="pt-BR", tz=180)
        pytrends.build_payload([keyword], cat=0, timeframe="today 3-m", geo=geo)

        region_data = pytrends.interest_by_region(resolution="REGION", inc_low_vol=True, inc_geo_code=True)

        if region_data.empty:
            return f"Sem dados regionais para: {keyword}"

        # Sort by interest descending and get top 15
        sorted_data = region_data.sort_values(by=keyword, ascending=False).head(15)
        result = {
            "keyword": keyword,
            "geo": geo,
            "regions": [],
        }

        for region_name, row in sorted_data.iterrows():
            interest_value = int(row[keyword])
            if interest_value > 0:
                result["regions"].append({
                    "region": str(region_name),
                    "interest": interest_value,
                })

        if not result["regions"]:
            return f"Interesse regional muito baixo para: {keyword}"

        return str(result)
    except ImportError:
        return "pytrends nao instalado. Execute: pip install pytrends"
    except Exception as e:
        return f"Erro ao buscar interesse regional: {e}"


@tool
def get_related_topics(keyword: str, geo: str = "BR") -> str:
    """Busca topicos relacionados a uma keyword no Google Trends. Retorna topicos mais pesquisados e em ascensao."""
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="pt-BR", tz=180)
        pytrends.build_payload([keyword], cat=0, timeframe="today 3-m", geo=geo)

        topics = pytrends.related_topics()
        result = {"keyword": keyword, "geo": geo, "top_topics": [], "rising_topics": []}

        if keyword in topics:
            top = topics[keyword].get("top")
            rising = topics[keyword].get("rising")

            if top is not None and not top.empty:
                for _, row in top.head(10).iterrows():
                    result["top_topics"].append({
                        "title": row.get("topic_title", ""),
                        "type": row.get("topic_type", ""),
                        "value": int(row.get("value", 0)),
                    })

            if rising is not None and not rising.empty:
                for _, row in rising.head(10).iterrows():
                    result["rising_topics"].append({
                        "title": row.get("topic_title", ""),
                        "type": row.get("topic_type", ""),
                        "value": str(row.get("value", "")),
                    })

        if not result["top_topics"] and not result["rising_topics"]:
            return f"Sem topicos relacionados encontrados para: {keyword}"

        return str(result)
    except ImportError:
        return "pytrends nao instalado. Execute: pip install pytrends"
    except Exception as e:
        return f"Erro ao buscar topicos relacionados: {e}"


def get_trends_tools():
    return [
        get_google_trends,
        get_related_queries,
        get_trending_searches,
        get_interest_by_region,
        get_related_topics,
    ]
