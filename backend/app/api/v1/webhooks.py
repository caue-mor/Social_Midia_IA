from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/instagram")
async def instagram_webhook(request: Request):
    """Webhook para notificacoes do Instagram Graph API."""
    body = await request.json()
    # TODO: Processar notificacoes do Instagram
    return {"status": "received"}


@router.get("/instagram")
async def instagram_webhook_verify(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None,
):
    """Verificacao do webhook do Instagram."""
    from app.config import get_settings
    settings = get_settings()
    # TODO: Implementar verificacao com token
    if hub_mode == "subscribe" and hub_challenge:
        return int(hub_challenge)
    return {"error": "Invalid verification"}


@router.post("/youtube")
async def youtube_webhook(request: Request):
    """Webhook para notificacoes do YouTube."""
    body = await request.body()
    # TODO: Processar notificacoes PubSubHubbub do YouTube
    return {"status": "received"}
