"""Orquestrador do pipeline de conteudo.

Executa a sequencia: AUDIT -> PLAN -> CONTENT -> SCRIPTS -> QUALITY GATE -> PERSIST.
Cada step usa validate_and_retry para garantir output JSON estruturado.
"""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Awaitable, Callable, Optional

from app.agents.calendar_planner import create_calendar_planner
from app.agents.content_writer import create_content_writer
from app.agents.quality_gate import create_quality_gate
from app.agents.social_analyst import create_social_analyst
from app.agents.video_script_writer import create_video_script_writer
from app.constants import TABLES
from app.models.contracts import (
    AuditReport,
    ContentPieceContract,
    MonthlyPlan,
    PipelineResult,
    PipelineStep,
    QualityReport,
    ScriptReel,
    WeeklyPlan,
)
from app.prompts.audit.v1 import PROMPT_VERSION as AUDIT_V
from app.prompts.audit.v1 import build_prompt as build_audit_prompt
from app.prompts.content.v1 import PROMPT_VERSION as CONTENT_V
from app.prompts.content.v1 import build_prompt as build_content_prompt
from app.prompts.plan.v1 import PROMPT_VERSION as PLAN_V
from app.prompts.plan.v1 import build_prompt as build_plan_prompt
from app.prompts.quality.v1 import PROMPT_VERSION as QUALITY_V
from app.prompts.quality.v1 import build_prompt as build_quality_prompt
from app.prompts.scripts.v1 import PROMPT_VERSION as SCRIPTS_V
from app.prompts.scripts.v1 import build_prompt as build_scripts_prompt
from app.services.contract_validator import validate_and_retry

logger = logging.getLogger("agentesocial.pipeline")

ProgressCallback = Callable[[str, str], Awaitable[None]]


class PipelineService:
    async def execute(
        self,
        user_id: str,
        config: dict,
        progress_cb: Optional[ProgressCallback] = None,
    ) -> PipelineResult:
        """Executa o pipeline completo de geracao de conteudo.

        Args:
            user_id: ID do usuario
            config: Configuracao do pipeline (period, platforms, focus_topics, include_video)
            progress_cb: Callback async para enviar progresso (step_name, message)

        Returns:
            PipelineResult com todos os outputs dos steps
        """
        pipeline_id = str(uuid.uuid4())
        period = config.get("period", "weekly")
        platforms = config.get("platforms", ["instagram", "youtube", "tiktok", "linkedin"])
        focus_topics = config.get("focus_topics")
        include_video = config.get("include_video", True)

        result = PipelineResult(
            pipeline_id=pipeline_id,
            user_id=user_id,
            config=config,
            prompt_versions={
                "audit": AUDIT_V,
                "plan": PLAN_V,
                "content": CONTENT_V,
                "scripts": SCRIPTS_V,
                "quality": QUALITY_V,
            },
            created_at=datetime.utcnow().isoformat(),
        )

        async def notify(step: str, message: str):
            if progress_cb:
                await progress_cb(step, message)

        # --- Step 1: AUDIT ---
        await notify("audit", "Auditando perfil...")
        audit_step = PipelineStep(name="audit", status="running", started_at=datetime.utcnow().isoformat())
        result.steps.append(audit_step)

        try:
            audit_prompt = build_audit_prompt(user_id, platforms, focus_topics)
            audit_model, _ = await validate_and_retry(
                create_social_analyst, audit_prompt, AuditReport, user_id,
            )
            result.audit_result = audit_model.model_dump()
            audit_step.status = "completed"
            audit_step.completed_at = datetime.utcnow().isoformat()
        except Exception as e:
            logger.error("Audit step failed: %s", e)
            audit_step.status = "failed"
            audit_step.error = str(e)
            audit_step.completed_at = datetime.utcnow().isoformat()
            result.audit_result = AuditReport().model_dump()

        # --- Step 2: PLAN ---
        await notify("plan", "Gerando plano editorial...")
        plan_step = PipelineStep(name="plan", status="running", started_at=datetime.utcnow().isoformat())
        result.steps.append(plan_step)

        plan_schema = MonthlyPlan if period == "monthly" else WeeklyPlan
        plan_slots: list[dict] = []

        try:
            audit_summary = result.audit_result or {}
            plan_prompt = build_plan_prompt(audit_summary, period, platforms, focus_topics)
            plan_model, _ = await validate_and_retry(
                create_calendar_planner, plan_prompt, plan_schema, user_id,
            )
            result.plan_result = plan_model.model_dump()
            plan_step.status = "completed"
            plan_step.completed_at = datetime.utcnow().isoformat()

            # Extrair slots para os proximos steps
            if period == "monthly" and hasattr(plan_model, "weeks"):
                for week in plan_model.weeks:
                    plan_slots.extend([s.model_dump() for s in week.slots])
            elif hasattr(plan_model, "slots"):
                plan_slots = [s.model_dump() for s in plan_model.slots]
        except Exception as e:
            logger.error("Plan step failed: %s", e)
            plan_step.status = "failed"
            plan_step.error = str(e)
            plan_step.completed_at = datetime.utcnow().isoformat()

        # --- Step 3: CONTENT ---
        await notify("content", "Criando conteudo...")
        content_step = PipelineStep(name="content", status="running", started_at=datetime.utcnow().isoformat())
        result.steps.append(content_step)

        try:
            for slot in plan_slots:
                content_prompt = build_content_prompt(slot)
                content_model, _ = await validate_and_retry(
                    create_content_writer, content_prompt, ContentPieceContract, user_id,
                )
                result.content_results.append(content_model.model_dump())
            content_step.status = "completed"
            content_step.completed_at = datetime.utcnow().isoformat()
        except Exception as e:
            logger.error("Content step failed: %s", e)
            content_step.status = "failed"
            content_step.error = str(e)
            content_step.completed_at = datetime.utcnow().isoformat()

        # --- Step 4: SCRIPTS (se include_video) ---
        if include_video:
            await notify("video_scripts", "Escrevendo roteiros...")
            scripts_step = PipelineStep(name="video_scripts", status="running", started_at=datetime.utcnow().isoformat())
            result.steps.append(scripts_step)

            try:
                video_types = {"reel", "shorts", "video_longo", "tiktok"}
                video_slots = [s for s in plan_slots if s.get("content_type", "").lower().replace(" ", "_") in video_types]

                for slot in video_slots:
                    ct = slot.get("content_type", "reel").lower().replace(" ", "_")
                    script_type = "youtube" if ct in ("video_longo", "shorts") else "reel"
                    scripts_prompt = build_scripts_prompt(slot, script_type)
                    script_model, _ = await validate_and_retry(
                        create_video_script_writer, scripts_prompt, ScriptReel, user_id,
                    )
                    result.script_results.append(script_model.model_dump())
                scripts_step.status = "completed"
                scripts_step.completed_at = datetime.utcnow().isoformat()
            except Exception as e:
                logger.error("Scripts step failed: %s", e)
                scripts_step.status = "failed"
                scripts_step.error = str(e)
                scripts_step.completed_at = datetime.utcnow().isoformat()

        # --- Step 5: QUALITY GATE ---
        await notify("quality_gate", "Validando qualidade...")
        qg_step = PipelineStep(name="quality_gate", status="running", started_at=datetime.utcnow().isoformat())
        result.steps.append(qg_step)

        try:
            all_content = result.content_results + result.script_results
            quality_prompt = build_quality_prompt(all_content, plan_slots)
            qr_model, _ = await validate_and_retry(
                create_quality_gate, quality_prompt, QualityReport, user_id,
            )
            result.quality_report = qr_model.model_dump()
            qg_step.status = "completed"
            qg_step.completed_at = datetime.utcnow().isoformat()
        except Exception as e:
            logger.error("Quality gate step failed: %s", e)
            qg_step.status = "failed"
            qg_step.error = str(e)
            qg_step.completed_at = datetime.utcnow().isoformat()

        # --- Step 6: PERSIST ---
        result.status = "completed"
        result.completed_at = datetime.utcnow().isoformat()

        # Calcula version auto-increment
        version = await self._next_version(user_id)
        result.version = version

        await self._persist(result)
        await self._persist_content_and_calendar(result, plan_slots)

        return result

    async def _next_version(self, user_id: str) -> int:
        """Calcula proximo version para o usuario."""
        try:
            from app.database.supabase_client import get_supabase_admin
            supabase = get_supabase_admin()
            res = (
                supabase.table(TABLES["pipeline_runs"])
                .select("version")
                .eq("user_id", user_id)
                .order("version", desc=True)
                .limit(1)
                .execute()
            )
            if res.data:
                return res.data[0]["version"] + 1
            return 1
        except Exception as e:
            logger.warning("Could not fetch version, defaulting to 1: %s", e)
            return 1

    async def _persist(self, result: PipelineResult) -> None:
        """Persiste o resultado do pipeline no Supabase."""
        try:
            from app.database.supabase_client import get_supabase_admin
            supabase = get_supabase_admin()
            supabase.table(TABLES["pipeline_runs"]).insert({
                "id": result.pipeline_id,
                "user_id": result.user_id,
                "version": result.version,
                "status": result.status,
                "config": result.config,
                "audit_result": result.audit_result,
                "plan_result": result.plan_result,
                "content_results": result.content_results,
                "quality_report": result.quality_report,
                "created_at": result.created_at,
                "completed_at": result.completed_at,
            }).execute()
            logger.info("Pipeline %s persisted (version=%d)", result.pipeline_id, result.version)
        except Exception as e:
            logger.error("Failed to persist pipeline result: %s", e)

    async def _persist_content_and_calendar(
        self, result: PipelineResult, plan_slots: list[dict]
    ) -> None:
        """Persiste content_pieces e calendar_events derivados do pipeline.

        Insere um content_piece para cada content_result e um calendar_event
        correspondente linkado via content_id. Falhas sao logadas mas NAO
        quebram o pipeline (resultado ja foi salvo em pipeline_runs).
        """
        if not result.content_results:
            return

        try:
            from app.database.supabase_client import get_supabase_admin
            supabase = get_supabase_admin()
        except Exception as e:
            logger.warning("Could not get supabase client for content/calendar persist: %s", e)
            return

        for i, content in enumerate(result.content_results):
            slot = plan_slots[i] if i < len(plan_slots) else {}
            content_piece_id = str(uuid.uuid4())

            # --- Insert content_piece ---
            try:
                body = content.get("body") or ""
                if not body:
                    hook = content.get("hook", "")
                    caption = content.get("caption", "")
                    body = f"{hook}\n\n{caption}".strip() if hook or caption else ""

                metadata = {
                    "hook": content.get("hook", ""),
                    "cta": content.get("cta", ""),
                    "slides": content.get("slides", []),
                    "story_frames": content.get("story_frames", []),
                    "thread_tweets": content.get("thread_tweets", []),
                    "word_count": content.get("word_count", 0),
                    "pipeline_run_id": result.pipeline_id,
                }

                supabase.table(TABLES["content_pieces"]).insert({
                    "id": content_piece_id,
                    "user_id": result.user_id,
                    "content_type": content.get("content_type", ""),
                    "platform": content.get("platform", ""),
                    "title": content.get("title", ""),
                    "body": body,
                    "caption": content.get("caption", ""),
                    "hashtags": content.get("hashtags", []),
                    "visual_suggestion": content.get("visual_suggestion", ""),
                    "status": "draft",
                    "metadata": metadata,
                }).execute()

                result.content_piece_ids.append(content_piece_id)
                logger.info("Content piece %s created (slot %d)", content_piece_id, i)
            except Exception as e:
                logger.warning("Failed to insert content_piece for slot %d: %s", i, e)
                continue  # skip calendar event if content_piece failed

            # --- Insert calendar_event ---
            try:
                scheduled_at = None
                sched_date = slot.get("scheduled_date", "")
                sched_time = slot.get("scheduled_time", "")
                if sched_date and sched_time:
                    scheduled_at = f"{sched_date}T{sched_time}"
                elif sched_date:
                    scheduled_at = f"{sched_date}T09:00:00"

                if not scheduled_at:
                    fallback_dt = datetime.utcnow().replace(
                        hour=9, minute=0, second=0, microsecond=0
                    )
                    fallback_dt = fallback_dt + timedelta(hours=i * 6)
                    scheduled_at = fallback_dt.isoformat()

                title = slot.get("title", "")
                if not title:
                    plat = slot.get("platform", content.get("platform", ""))
                    ctype = slot.get("content_type", content.get("content_type", ""))
                    title = f"{plat} - {ctype}".strip(" -")

                notes = slot.get("notes") or slot.get("topic", "")

                calendar_event_id = str(uuid.uuid4())

                supabase.table(TABLES["content_calendar"]).insert({
                    "id": calendar_event_id,
                    "user_id": result.user_id,
                    "title": title,
                    "content_id": content_piece_id,
                    "platform": slot.get("platform", content.get("platform", "")),
                    "scheduled_at": scheduled_at,
                    "status": "scheduled",
                    "notes": notes,
                }).execute()

                result.calendar_event_ids.append(calendar_event_id)
                logger.info("Calendar event %s created for content %s", calendar_event_id, content_piece_id)
            except Exception as e:
                logger.warning("Failed to insert calendar_event for slot %d: %s", i, e)
