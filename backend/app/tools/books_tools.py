import httpx
from agno.tools import tool

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


@tool
def search_books(query: str, max_results: int = 5, language: str = "pt") -> str:
    """Busca livros na Google Books API. Retorna titulo, autores, editora, data de publicacao,
    descricao, numero de paginas, categorias e link de preview. Util para encontrar referencias
    bibliograficas e recomendar leituras ao usuario.

    Args:
        query: Termo de busca (titulo, autor ou tema).
        max_results: Numero maximo de resultados (1-10). Default: 5.
        language: Codigo do idioma para filtrar resultados. Default: 'pt' (portugues).

    Returns:
        String formatada com detalhes dos livros encontrados.
    """
    try:
        max_results = max(1, min(max_results, 10))

        params = {
            "q": query,
            "maxResults": max_results,
            "langRestrict": language,
            "orderBy": "relevance",
            "printType": "books",
        }

        with httpx.Client(timeout=15.0) as client:
            response = client.get(GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

        total_items = data.get("totalItems", 0)
        if total_items == 0 or "items" not in data:
            return f"Nenhum livro encontrado para: '{query}'"

        books = []
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            book = {
                "titulo": info.get("title", "Sem titulo"),
                "autores": ", ".join(info.get("authors", ["Autor desconhecido"])),
                "editora": info.get("publisher", "Editora nao informada"),
                "data_publicacao": info.get("publishedDate", "Data nao informada"),
                "descricao": _truncate(info.get("description", "Sem descricao"), 300),
                "paginas": info.get("pageCount", "N/A"),
                "categorias": ", ".join(info.get("categories", [])),
                "link_preview": info.get("previewLink", ""),
            }
            books.append(book)

        result_lines = [f"Encontrados {total_items} livros para '{query}'. Mostrando {len(books)}:\n"]
        for i, book in enumerate(books, 1):
            result_lines.append(
                f"--- Livro {i} ---\n"
                f"Titulo: {book['titulo']}\n"
                f"Autores: {book['autores']}\n"
                f"Editora: {book['editora']}\n"
                f"Publicacao: {book['data_publicacao']}\n"
                f"Paginas: {book['paginas']}\n"
                f"Categorias: {book['categorias']}\n"
                f"Descricao: {book['descricao']}\n"
                f"Preview: {book['link_preview']}\n"
            )

        return "\n".join(result_lines)

    except httpx.TimeoutException:
        return "Erro: Timeout ao conectar com Google Books API. Tente novamente."
    except httpx.HTTPStatusError as e:
        return f"Erro HTTP da Google Books API: {e.response.status_code}"
    except Exception as e:
        return f"Erro ao buscar livros: {e}"


@tool
def search_books_by_topic(topic: str, category: str = "") -> str:
    """Busca livros relacionados a um topico de marketing, negocios ou redes sociais.
    Adiciona contexto de 'marketing digital' ou 'social media' automaticamente para
    encontrar referencias relevantes para estrategias de conteudo.

    Args:
        topic: Topico principal (ex: 'copywriting', 'branding', 'growth hacking').
        category: Categoria opcional para refinar busca (ex: 'marketing', 'business', 'psychology').

    Returns:
        String formatada com livros relevantes ao topico.
    """
    try:
        search_query = f"{topic} marketing digital"
        if category:
            search_query = f"{topic}+subject:{category}"

        params = {
            "q": search_query,
            "maxResults": 5,
            "orderBy": "relevance",
            "printType": "books",
        }

        with httpx.Client(timeout=15.0) as client:
            response = client.get(GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

        total_items = data.get("totalItems", 0)
        if total_items == 0 or "items" not in data:
            return f"Nenhum livro encontrado para o topico: '{topic}'"

        books = []
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            book = {
                "titulo": info.get("title", "Sem titulo"),
                "autores": ", ".join(info.get("authors", ["Autor desconhecido"])),
                "descricao": _truncate(info.get("description", "Sem descricao"), 200),
                "categorias": ", ".join(info.get("categories", [])),
                "link_preview": info.get("previewLink", ""),
            }
            books.append(book)

        result_lines = [f"Livros sobre '{topic}' (total encontrado: {total_items}):\n"]
        for i, book in enumerate(books, 1):
            result_lines.append(
                f"{i}. \"{book['titulo']}\" - {book['autores']}\n"
                f"   Categorias: {book['categorias']}\n"
                f"   Resumo: {book['descricao']}\n"
                f"   Preview: {book['link_preview']}\n"
            )

        return "\n".join(result_lines)

    except httpx.TimeoutException:
        return "Erro: Timeout ao conectar com Google Books API. Tente novamente."
    except httpx.HTTPStatusError as e:
        return f"Erro HTTP da Google Books API: {e.response.status_code}"
    except Exception as e:
        return f"Erro ao buscar livros por topico: {e}"


@tool
def get_book_quotes_suggestions(book_title: str, author: str = "") -> str:
    """Busca detalhes de um livro especifico para ajudar a gerar citacoes e referencias
    relevantes. Retorna descricao completa, categorias e contexto do livro.

    Args:
        book_title: Titulo do livro (ex: 'Isso e Marketing').
        author: Nome do autor para refinar a busca (ex: 'Seth Godin').

    Returns:
        String com detalhes do livro para contexto de citacoes.
    """
    try:
        search_query = f'intitle:"{book_title}"'
        if author:
            search_query += f'+inauthor:"{author}"'

        params = {
            "q": search_query,
            "maxResults": 3,
            "orderBy": "relevance",
            "printType": "books",
        }

        with httpx.Client(timeout=15.0) as client:
            response = client.get(GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

        total_items = data.get("totalItems", 0)
        if total_items == 0 or "items" not in data:
            return f"Livro nao encontrado: '{book_title}'" + (f" de {author}" if author else "")

        result_lines = []
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            titulo = info.get("title", "Sem titulo")
            autores = ", ".join(info.get("authors", ["Autor desconhecido"]))
            descricao = info.get("description", "Sem descricao disponivel")
            categorias = ", ".join(info.get("categories", []))
            data_pub = info.get("publishedDate", "Data nao informada")
            paginas = info.get("pageCount", "N/A")
            subtitulo = info.get("subtitle", "")
            editora = info.get("publisher", "Editora nao informada")

            titulo_completo = f"{titulo}: {subtitulo}" if subtitulo else titulo

            result_lines.append(
                f"=== {titulo_completo} ===\n"
                f"Autor(es): {autores}\n"
                f"Editora: {editora}\n"
                f"Publicacao: {data_pub}\n"
                f"Paginas: {paginas}\n"
                f"Categorias: {categorias}\n"
                f"\nDescricao completa:\n{descricao}\n"
                f"\n---\n"
                f"Use estas informacoes para contextualizar citacoes e referencias.\n"
                f"O conteudo do livro gira em torno dos temas acima.\n"
                f"Gere citacoes que reflitam o espirito e as ideias centrais do livro.\n"
            )

        return "\n".join(result_lines)

    except httpx.TimeoutException:
        return "Erro: Timeout ao conectar com Google Books API. Tente novamente."
    except httpx.HTTPStatusError as e:
        return f"Erro HTTP da Google Books API: {e.response.status_code}"
    except Exception as e:
        return f"Erro ao buscar detalhes do livro: {e}"


def _truncate(text: str, max_length: int) -> str:
    """Trunca texto ao comprimento maximo, adicionando reticencias se necessario."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."


def get_books_tools() -> list:
    """Retorna todas as tools de busca de livros."""
    return [
        search_books,
        search_books_by_topic,
        get_book_quotes_suggestions,
    ]
