"""Contratos Pydantic para output estruturado dos agentes do pipeline.

Cada agente do pipeline retorna JSON validado contra estes schemas.
Campos com defaults permitem fallback graceful quando validacao falha.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# --- Enums ---


class Platform(str, Enum):
    instagram = "instagram"
    youtube = "youtube"
    tiktok = "tiktok"
    linkedin = "linkedin"
    twitter = "twitter"
    facebook = "facebook"


class ContentType(str, Enum):
    post = "post"
    carrossel = "carrossel"
    reel = "reel"
    story = "story"
    thread = "thread"
    video_longo = "video_longo"
    shorts = "shorts"
    podcast = "podcast"


class QualityVerdict(str, Enum):
    passed = "passed"
    warn = "warn"
    fail = "fail"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


# --- Audit ---


class ContentPillar(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = ""
    description: str = ""
    percentage: float = 0.0
    examples: list[str] = Field(default_factory=list)


class CompetitorEntry(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = ""
    platform: str = ""
    followers: int = 0
    engagement_rate: float = 0.0
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class AuditReport(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    pillars: list[ContentPillar] = Field(default_factory=list, description="Pilares de conteudo identificados")
    posting_frequency: dict[str, int] = Field(default_factory=dict, description="Frequencia por plataforma (posts/semana)")
    best_posting_times: dict[str, list[str]] = Field(default_factory=dict, description="Melhores horarios por plataforma")
    engagement_rate: dict[str, float] = Field(default_factory=dict, description="Taxa de engajamento por plataforma")
    competitors: list[CompetitorEntry] = Field(default_factory=list, description="Concorrentes analisados")
    strengths: list[str] = Field(default_factory=list, description="Pontos fortes do perfil")
    weaknesses: list[str] = Field(default_factory=list, description="Pontos fracos do perfil")
    opportunities: list[str] = Field(default_factory=list, description="Oportunidades identificadas")
    recommendations: list[str] = Field(default_factory=list, description="Recomendacoes priorizadas")
    _raw_text: Optional[str] = None


# --- Plan ---


class PlanSlot(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = ""
    platform: str = ""
    content_type: str = ""
    scheduled_date: str = ""
    scheduled_time: str = ""
    topic: str = ""
    pillar: str = ""
    notes: str = ""
    status: str = "draft"


class WeeklyPlan(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    week_number: int = 1
    start_date: str = ""
    end_date: str = ""
    slots: list[PlanSlot] = Field(default_factory=list, description="Slots de conteudo da semana")
    total_posts: int = 0
    platforms_covered: list[str] = Field(default_factory=list)
    _raw_text: Optional[str] = None


class MonthlyPlan(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    month: str = ""
    year: int = 0
    weeks: list[WeeklyPlan] = Field(default_factory=list, description="Planos semanais do mes")
    total_posts: int = 0
    seasonal_dates: list[str] = Field(default_factory=list, description="Datas sazonais do mes")
    _raw_text: Optional[str] = None


# --- Content ---


class ContentPieceContract(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = ""
    platform: str = ""
    content_type: str = ""
    hook: str = Field(default="", description="Frase de abertura que prende atencao")
    body: str = ""
    caption: str = ""
    cta: str = Field(default="", description="Call to action")
    hashtags: list[str] = Field(default_factory=list)
    visual_suggestion: str = ""
    slides: list[dict] = Field(default_factory=list, description="Slides do carrossel (se aplicavel)")
    story_frames: list[dict] = Field(default_factory=list, description="Frames do story (se aplicavel)")
    thread_tweets: list[str] = Field(default_factory=list, description="Tweets da thread (se aplicavel)")
    word_count: int = 0
    _raw_text: Optional[str] = None


# --- Scripts ---


class ScriptBlock(BaseModel):
    timestamp: str = ""
    visual: str = ""
    speech: str = ""
    text_overlay: str = ""
    effect: str = ""
    notes: str = ""


class ScriptReel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = ""
    platform: str = ""
    duration_seconds: int = 30
    hook: str = ""
    blocks: list[ScriptBlock] = Field(default_factory=list)
    audio_suggestion: str = ""
    hashtags: list[str] = Field(default_factory=list)
    caption: str = ""
    _raw_text: Optional[str] = None


class ScriptChapter(BaseModel):
    title: str = ""
    timestamp_start: str = ""
    timestamp_end: str = ""
    speech: str = ""
    visual: str = ""
    b_roll: list[str] = Field(default_factory=list)
    text_overlay: str = ""
    retention_cue: str = ""


class ScriptYouTube(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = ""
    title_alt: str = ""
    duration_minutes: int = 10
    chapters: list[ScriptChapter] = Field(default_factory=list)
    description_seo: str = ""
    tags: list[str] = Field(default_factory=list)
    thumbnail_brief: str = ""
    timestamps: list[str] = Field(default_factory=list)
    _raw_text: Optional[str] = None


class PodcastBlock(BaseModel):
    timestamp: str = ""
    section: str = ""
    content: str = ""
    notes: str = ""


class PodcastClip(BaseModel):
    title: str = ""
    timestamp_start: str = ""
    timestamp_end: str = ""
    platform_target: str = ""
    viral_score: int = 5
    caption: str = ""
    hashtags: list[str] = Field(default_factory=list)


class ScriptPodcast(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str = ""
    episode_number: int = 0
    duration_minutes: int = 30
    blocks: list[PodcastBlock] = Field(default_factory=list)
    show_notes: str = ""
    clips: list[PodcastClip] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    _raw_text: Optional[str] = None


# --- Hashtags ---


class HashtagBlock(BaseModel):
    category: str = ""  # alto_volume, medio_volume, nicho
    hashtags: list[str] = Field(default_factory=list)
    volume_range: str = ""
    notes: str = ""


class HashtagStrategy(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    platform: str = ""
    total_hashtags: int = 0
    blocks: list[HashtagBlock] = Field(default_factory=list)
    banned_hashtags: list[str] = Field(default_factory=list, description="Hashtags a evitar")
    rotation_tip: str = ""
    _raw_text: Optional[str] = None


# --- Quality Gate ---


class QualityCheck(BaseModel):
    name: str = ""
    passed: bool = True
    severity: str = "low"
    message: str = ""
    details: str = ""


class QualityReport(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    verdict: str = "passed"
    score: int = 100
    checks: list[QualityCheck] = Field(default_factory=list)
    summary: str = ""
    recommendations: list[str] = Field(default_factory=list)
    _raw_text: Optional[str] = None


# --- Pipeline ---


class PipelineStep(BaseModel):
    name: str = ""
    status: str = "pending"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


class PipelineResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    pipeline_id: str = ""
    user_id: str = ""
    version: int = 1
    status: str = "running"
    config: dict = Field(default_factory=dict)
    prompt_versions: dict[str, str] = Field(default_factory=dict)
    steps: list[PipelineStep] = Field(default_factory=list)
    audit_result: Optional[dict] = None
    plan_result: Optional[dict] = None
    content_results: list[dict] = Field(default_factory=list)
    script_results: list[dict] = Field(default_factory=list)
    quality_report: Optional[dict] = None
    content_piece_ids: list[str] = Field(default_factory=list)
    calendar_event_ids: list[str] = Field(default_factory=list)
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
