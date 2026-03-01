"""Router FastAPI para o pipeline de conteudo.

Endpoints:
- POST /generate         — Execucao sincrona, retorna PipelineResult completo
- POST /generate/stream  — SSE streaming com progresso por step
- GET  /runs             — Lista runs do usuario (paginado)
- GET  /runs/{pipeline_id} — Detalhe de uma run
"""

import asyncio
import json
import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.constants import TABLES
from app.dependencies import get_current_user
from app.services.pipeline_service import PipelineService

router = APIRouter()
logger = logging.getLogger("agentesocial.pipeline_api")


class PipelineRequest(BaseModel):
    period: str = "weekly"
    platforms: list[str] = ["instagram", "youtube", "tiktok", "linkedin"]
    focus_topics: Optional[list[str]] = None
    include_video: bool = True


@router.post("/generate")
async def generate_pipeline(
    request: PipelineRequest,
    user: dict = Depends(get_current_user),
):
    """Executa o pipeline completo de forma sincrona."""
    service = PipelineService()
    result = await service.execute(
        user_id=user["id"],
        config=request.model_dump(),
    )
    return result.model_dump()


@router.post("/generate/stream")
async def generate_pipeline_stream(
    request: PipelineRequest,
    user: dict = Depends(get_current_user),
):
    """Executa o pipeline com SSE streaming de progresso por step."""
    service = PipelineService()

    async def event_stream():
        yield f"data: {json.dumps({'type': 'progress', 'step': 'init', 'message': 'Iniciando pipeline...'})}\n\n"

        result_holder: dict = {}
        error_holder: dict = {}
        done_event = asyncio.Event()
        progress_queue: asyncio.Queue = asyncio.Queue()

        async def progress_cb(step: str, message: str):
            await progress_queue.put({"step": step, "message": message})

        async def run_pipeline():
            try:
                result = await service.execute(
                    user_id=user["id"],
                    config=request.model_dump(),
                    progress_cb=progress_cb,
                )
                result_holder["data"] = result
            except Exception as e:
                error_holder["error"] = str(e)
            finally:
                done_event.set()

        task = asyncio.create_task(run_pipeline())

        while not done_event.is_set():
            try:
                progress = await asyncio.wait_for(progress_queue.get(), timeout=5.0)
                yield f"data: {json.dumps({'type': 'progress', **progress})}\n\n"
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"

        # Drain remaining progress messages
        while not progress_queue.empty():
            try:
                progress = progress_queue.get_nowait()
                yield f"data: {json.dumps({'type': 'progress', **progress})}\n\n"
            except asyncio.QueueEmpty:
                break

        await task

        if "error" in error_holder:
            yield f"data: {json.dumps({'type': 'error', 'message': error_holder['error']})}\n\n"
        elif "data" in result_holder:
            yield f"data: {json.dumps({'type': 'complete', 'data': result_holder['data'].model_dump()}, default=str)}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Resultado vazio'})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/runs")
async def list_pipeline_runs(
    user: dict = Depends(get_current_user),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Lista pipeline runs do usuario, paginado."""
    from app.database.supabase_client import get_supabase_admin
    supabase = get_supabase_admin()

    try:
        result = (
            supabase.table(TABLES["pipeline_runs"])
            .select("id,version,status,config,created_at,completed_at")
            .eq("user_id", user["id"])
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return {"runs": result.data, "limit": limit, "offset": offset}
    except Exception as e:
        logger.error("Error listing pipeline runs: %s", e)
        raise HTTPException(status_code=500, detail="Erro ao listar pipeline runs")


@router.get("/runs/{pipeline_id}")
async def get_pipeline_run(
    pipeline_id: str,
    user: dict = Depends(get_current_user),
):
    """Retorna detalhe completo de uma pipeline run."""
    from app.database.supabase_client import get_supabase_admin
    supabase = get_supabase_admin()

    try:
        result = (
            supabase.table(TABLES["pipeline_runs"])
            .select("*")
            .eq("id", pipeline_id)
            .eq("user_id", user["id"])
            .maybe_single()
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Pipeline run nao encontrada")
        return result.data
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting pipeline run %s: %s", pipeline_id, e)
        raise HTTPException(status_code=500, detail="Erro ao buscar pipeline run")
