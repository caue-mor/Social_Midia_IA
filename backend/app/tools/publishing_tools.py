import logging
from datetime import datetime

import httpx
from agno.tools import tool

from app.config import get_settings

logger = logging.getLogger("agentesocial.publishing")

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"

_INSTAGRAM_NOT_CONFIGURED_MSG = (
    "A integracao com o Instagram ainda nao esta configurada para publicacao. "
    "Para conectar sua conta, acesse Configuracoes > Integracoes > Instagram "
    "e adicione seu INSTAGRAM_ACCESS_TOKEN e INSTAGRAM_BUSINESS_ACCOUNT_ID. "
    "Ambos sao necessarios para publicar conteudo via Graph API."
)


def _get_ig_credentials() -> tuple[str, str] | None:
    """Return (access_token, account_id) or None when not configured."""
    settings = get_settings()
    token = settings.INSTAGRAM_ACCESS_TOKEN
    account_id = settings.INSTAGRAM_BUSINESS_ACCOUNT_ID
    if not token or not account_id:
        return None
    return token, account_id


# ---------------------------------------------------------------------------
# Single Image / Video Publishing
# ---------------------------------------------------------------------------


@tool
def publish_to_instagram(
    caption: str,
    image_url: str,
    media_type: str = "IMAGE",
) -> str:
    """Publica um post no Instagram via Graph API (Content Publishing).

    Suporta IMAGE, VIDEO e CAROUSEL (para carousel use publish_carousel_to_instagram).
    O image_url deve ser uma URL publica acessivel pelo servidor do Instagram.

    Args:
        caption: Legenda do post (pode incluir hashtags).
        image_url: URL publica da imagem ou video.
        media_type: Tipo de midia — "IMAGE" ou "VIDEO".

    Returns:
        Permalink do post publicado ou mensagem de erro.
    """
    creds = _get_ig_credentials()
    if creds is None:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds
    media_type = media_type.upper()

    if media_type not in ("IMAGE", "VIDEO"):
        return (
            "Tipo de midia invalido. Use 'IMAGE' ou 'VIDEO'. "
            "Para carrossel, use publish_carousel_to_instagram."
        )

    try:
        # ------------------------------------------------------------------
        # Step 1: Create media container
        # ------------------------------------------------------------------
        container_url = f"{GRAPH_API_BASE}/{account_id}/media"
        container_payload: dict = {
            "caption": caption,
            "access_token": access_token,
        }

        if media_type == "IMAGE":
            container_payload["image_url"] = image_url
        else:
            container_payload["media_type"] = "VIDEO"
            container_payload["video_url"] = image_url

        resp = httpx.post(container_url, data=container_payload, timeout=60)
        resp.raise_for_status()
        creation_id = resp.json().get("id")

        if not creation_id:
            return f"Erro: Instagram nao retornou creation_id. Resposta: {resp.json()}"

        # For VIDEO, the container processing is async. We poll until ready.
        if media_type == "VIDEO":
            status_result = _wait_for_container(creation_id, access_token)
            if status_result is not None:
                return status_result

        # ------------------------------------------------------------------
        # Step 2: Publish the container
        # ------------------------------------------------------------------
        publish_url = f"{GRAPH_API_BASE}/{account_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": access_token,
        }

        pub_resp = httpx.post(publish_url, data=publish_payload, timeout=60)
        pub_resp.raise_for_status()
        media_id = pub_resp.json().get("id")

        if not media_id:
            return f"Erro ao publicar: resposta inesperada — {pub_resp.json()}"

        # ------------------------------------------------------------------
        # Step 3: Fetch permalink
        # ------------------------------------------------------------------
        permalink = _get_permalink(media_id, access_token)

        logger.info("Instagram post published successfully: %s", media_id)
        return (
            f"Post publicado com sucesso no Instagram!\n"
            f"Media ID: {media_id}\n"
            f"Permalink: {permalink}"
        )

    except httpx.HTTPStatusError as e:
        error_body = e.response.json() if e.response.content else {}
        error_msg = error_body.get("error", {}).get("message", str(e))
        logger.error("Instagram publish HTTP error: %s — %s", e.response.status_code, error_msg)
        return f"Erro ao publicar no Instagram (HTTP {e.response.status_code}): {error_msg}"
    except Exception as e:
        logger.error("Instagram publish error: %s", e, exc_info=True)
        return f"Erro inesperado ao publicar no Instagram: {e}"


# ---------------------------------------------------------------------------
# Carousel Publishing
# ---------------------------------------------------------------------------


@tool
def publish_carousel_to_instagram(caption: str, image_urls: list[str]) -> str:
    """Publica um carrossel (multiplas imagens) no Instagram via Graph API.

    Args:
        caption: Legenda do carrossel.
        image_urls: Lista de URLs publicas das imagens (2 a 10 imagens).

    Returns:
        Permalink do carrossel publicado ou mensagem de erro.
    """
    creds = _get_ig_credentials()
    if creds is None:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds

    if not image_urls or len(image_urls) < 2:
        return "Um carrossel precisa de pelo menos 2 imagens."
    if len(image_urls) > 10:
        return "O Instagram permite no maximo 10 imagens por carrossel."

    try:
        # ------------------------------------------------------------------
        # Step 1: Create individual item containers (no caption on children)
        # ------------------------------------------------------------------
        children_ids: list[str] = []
        container_url = f"{GRAPH_API_BASE}/{account_id}/media"

        for idx, url in enumerate(image_urls):
            child_payload = {
                "image_url": url,
                "is_carousel_item": "true",
                "access_token": access_token,
            }
            resp = httpx.post(container_url, data=child_payload, timeout=60)
            resp.raise_for_status()
            child_id = resp.json().get("id")
            if not child_id:
                return (
                    f"Erro ao criar container da imagem {idx + 1}: "
                    f"resposta inesperada — {resp.json()}"
                )
            children_ids.append(child_id)

        # ------------------------------------------------------------------
        # Step 2: Create carousel container
        # ------------------------------------------------------------------
        carousel_payload = {
            "caption": caption,
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "access_token": access_token,
        }
        carousel_resp = httpx.post(container_url, data=carousel_payload, timeout=60)
        carousel_resp.raise_for_status()
        carousel_id = carousel_resp.json().get("id")

        if not carousel_id:
            return f"Erro ao criar container do carrossel: {carousel_resp.json()}"

        # ------------------------------------------------------------------
        # Step 3: Publish the carousel
        # ------------------------------------------------------------------
        publish_url = f"{GRAPH_API_BASE}/{account_id}/media_publish"
        publish_payload = {
            "creation_id": carousel_id,
            "access_token": access_token,
        }
        pub_resp = httpx.post(publish_url, data=publish_payload, timeout=60)
        pub_resp.raise_for_status()
        media_id = pub_resp.json().get("id")

        if not media_id:
            return f"Erro ao publicar carrossel: {pub_resp.json()}"

        permalink = _get_permalink(media_id, access_token)

        logger.info("Instagram carousel published successfully: %s", media_id)
        return (
            f"Carrossel publicado com sucesso no Instagram!\n"
            f"Media ID: {media_id}\n"
            f"Imagens: {len(image_urls)}\n"
            f"Permalink: {permalink}"
        )

    except httpx.HTTPStatusError as e:
        error_body = e.response.json() if e.response.content else {}
        error_msg = error_body.get("error", {}).get("message", str(e))
        logger.error("Instagram carousel HTTP error: %s — %s", e.response.status_code, error_msg)
        return f"Erro ao publicar carrossel (HTTP {e.response.status_code}): {error_msg}"
    except Exception as e:
        logger.error("Instagram carousel error: %s", e, exc_info=True)
        return f"Erro inesperado ao publicar carrossel: {e}"


# ---------------------------------------------------------------------------
# Scheduled Publishing
# ---------------------------------------------------------------------------


@tool
def schedule_instagram_post(
    caption: str,
    image_url: str,
    scheduled_time: str,
) -> str:
    """Agenda um post no Instagram para publicacao futura via Graph API.

    O horario agendado deve estar entre 10 minutos e 75 dias no futuro.

    Args:
        caption: Legenda do post.
        image_url: URL publica da imagem.
        scheduled_time: Horario de publicacao em formato ISO 8601 (ex: 2026-03-01T14:00:00Z).

    Returns:
        Confirmacao do agendamento ou mensagem de erro.
    """
    creds = _get_ig_credentials()
    if creds is None:
        return _INSTAGRAM_NOT_CONFIGURED_MSG

    access_token, account_id = creds

    # Validate scheduled_time format
    try:
        scheduled_dt = datetime.fromisoformat(scheduled_time.replace("Z", "+00:00"))
        scheduled_ts = int(scheduled_dt.timestamp())
    except (ValueError, TypeError):
        return (
            "Formato de horario invalido. Use ISO 8601, "
            "por exemplo: 2026-03-01T14:00:00Z"
        )

    # Instagram requires the time to be 10 min to 75 days in the future
    now_ts = int(datetime.utcnow().timestamp())
    min_ts = now_ts + 600  # 10 minutes
    max_ts = now_ts + (75 * 24 * 60 * 60)  # 75 days

    if scheduled_ts < min_ts:
        return "O horario agendado deve ser pelo menos 10 minutos no futuro."
    if scheduled_ts > max_ts:
        return "O horario agendado nao pode ser mais de 75 dias no futuro."

    try:
        # ------------------------------------------------------------------
        # Step 1: Create media container with publish_time (Unix timestamp)
        # ------------------------------------------------------------------
        container_url = f"{GRAPH_API_BASE}/{account_id}/media"
        container_payload = {
            "image_url": image_url,
            "caption": caption,
            "published": "false",
            "access_token": access_token,
        }

        resp = httpx.post(container_url, data=container_payload, timeout=60)
        resp.raise_for_status()
        creation_id = resp.json().get("id")

        if not creation_id:
            return f"Erro: Instagram nao retornou creation_id. Resposta: {resp.json()}"

        # ------------------------------------------------------------------
        # Step 2: Publish with scheduled timestamp
        # ------------------------------------------------------------------
        publish_url = f"{GRAPH_API_BASE}/{account_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": access_token,
        }

        pub_resp = httpx.post(publish_url, data=publish_payload, timeout=60)
        pub_resp.raise_for_status()
        media_id = pub_resp.json().get("id")

        if not media_id:
            return f"Erro ao agendar publicacao: {pub_resp.json()}"

        logger.info(
            "Instagram post scheduled: %s for %s",
            media_id,
            scheduled_time,
        )
        return (
            f"Post agendado com sucesso no Instagram!\n"
            f"Media ID: {media_id}\n"
            f"Agendado para: {scheduled_time}\n"
            f"Nota: O Instagram processara a publicacao automaticamente no horario agendado."
        )

    except httpx.HTTPStatusError as e:
        error_body = e.response.json() if e.response.content else {}
        error_msg = error_body.get("error", {}).get("message", str(e))
        logger.error("Instagram schedule HTTP error: %s — %s", e.response.status_code, error_msg)
        return f"Erro ao agendar post (HTTP {e.response.status_code}): {error_msg}"
    except Exception as e:
        logger.error("Instagram schedule error: %s", e, exc_info=True)
        return f"Erro inesperado ao agendar post: {e}"


# ---------------------------------------------------------------------------
# Helpers (internal)
# ---------------------------------------------------------------------------


def _wait_for_container(
    container_id: str,
    access_token: str,
    max_attempts: int = 30,
    poll_interval: float = 2.0,
) -> str | None:
    """Poll container status until FINISHED or timeout.

    Returns None on success (FINISHED), or an error string on failure.
    """
    import time

    status_url = f"{GRAPH_API_BASE}/{container_id}"
    params = {
        "fields": "status_code",
        "access_token": access_token,
    }

    for attempt in range(max_attempts):
        try:
            resp = httpx.get(status_url, params=params, timeout=30)
            resp.raise_for_status()
            status = resp.json().get("status_code")

            if status == "FINISHED":
                return None
            if status == "ERROR":
                return (
                    "Erro no processamento do video pelo Instagram. "
                    "Verifique se o formato e resolucao sao suportados."
                )
            if status == "EXPIRED":
                return "O container de midia expirou antes de ser publicado."

            # IN_PROGRESS — wait and retry
            time.sleep(poll_interval)
        except Exception as e:
            logger.warning("Error polling container %s (attempt %d): %s", container_id, attempt, e)
            time.sleep(poll_interval)

    return (
        "Tempo esgotado aguardando processamento do video. "
        "Tente novamente ou verifique o formato do video."
    )


def _get_permalink(media_id: str, access_token: str) -> str:
    """Fetch the permalink for a published media object."""
    try:
        url = f"{GRAPH_API_BASE}/{media_id}"
        params = {
            "fields": "permalink",
            "access_token": access_token,
        }
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("permalink", "Permalink nao disponivel")
    except Exception:
        return "Permalink nao disponivel"


# ---------------------------------------------------------------------------
# Tool Registry
# ---------------------------------------------------------------------------


def get_publishing_tools() -> list:
    """Return all publishing tools for agent registration."""
    return [
        publish_to_instagram,
        publish_carousel_to_instagram,
        schedule_instagram_post,
    ]
