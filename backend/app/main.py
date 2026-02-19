import logging
import time
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.dependencies import get_current_user
from app.api.v1 import auth as auth_router, chat, content, analysis, reports, calendar, settings as settings_router, webhooks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("agentesocial")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AgenteSocial API starting...")
    yield
    logger.info("AgenteSocial API shutting down...")


settings = get_settings()

app = FastAPI(
    title="AgenteSocial API",
    description="Ecossistema de IA para gestao de redes sociais",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} {response.status_code} {duration}ms")
    return response


# Routers
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(calendar.router, prefix="/api/v1/calendar", tags=["Calendar"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])


@app.get("/")
async def root():
    return {"service": "agentesocial-api", "version": "0.1.0"}


@app.get("/health")
async def health():
    checks = {"api": "healthy"}
    try:
        from app.database.supabase_client import get_supabase
        supabase = get_supabase()
        supabase.table("social_midia_profiles").select("id").limit(1).execute()
        checks["supabase"] = "healthy"
    except Exception as e:
        logger.warning(f"Supabase health check failed: {e}")
        checks["supabase"] = "unhealthy"
    return {"status": "healthy", "service": "agentesocial-api", "version": "0.1.0", "checks": checks}


@app.post("/admin/clear-cache")
async def clear_cache_endpoint(user: dict = Depends(get_current_user)):
    from app.middleware.cache import clear_cache
    clear_cache()
    return {"status": "cache_cleared"}
