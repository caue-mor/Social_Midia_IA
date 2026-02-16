from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Chat
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    agent_type: Optional[str] = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_type: str
    metadata: Optional[dict] = None


# Content
class ContentGenerateRequest(BaseModel):
    content_type: str
    platform: str
    topic: Optional[str] = None
    tone: Optional[str] = None
    reference_url: Optional[str] = None
    brand_voice_id: Optional[str] = None
    additional_instructions: Optional[str] = None


class ContentResponse(BaseModel):
    id: str
    content_type: str
    platform: str
    title: Optional[str] = None
    body: str
    hashtags: list[str] = []
    caption: Optional[str] = None
    visual_suggestion: Optional[str] = None
    metadata: Optional[dict] = None


# Analysis
class ProfileAnalysisRequest(BaseModel):
    platform: str
    profile_handle: str


class TrendSearchRequest(BaseModel):
    keywords: list[str]
    platform: Optional[str] = None
    country: str = "BR"


# Reports
class ReportGenerateRequest(BaseModel):
    report_type: str
    period_start: str
    period_end: str
    include_sections: list[str] = ["overview", "content", "engagement", "growth"]


# Calendar
class CalendarEventCreate(BaseModel):
    title: str
    content_id: Optional[str] = None
    platform: str
    scheduled_at: datetime
    status: str = "scheduled"
    notes: Optional[str] = None


# Social Profiles
class SocialProfileCreate(BaseModel):
    platform: str
    handle: str
    access_token: Optional[str] = None
    platform_user_id: Optional[str] = None
