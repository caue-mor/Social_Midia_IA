# Mapeamento centralizado de nomes de tabelas do Supabase.
# Qualquer renomeacao futura so precisa ser feita aqui.

TABLES: dict[str, str] = {
    "profiles": "social_midia_profiles",
    "content_pieces": "social_midia_content_pieces",
    "content_calendar": "social_midia_content_calendar",
    "viral_content": "social_midia_viral_content",
    "hashtag_research": "social_midia_hashtag_research",
    "podcast_episodes": "social_midia_podcast_episodes",
    "reports": "social_midia_reports",
    "analytics_snapshots": "social_midia_analytics_snapshots",
    "brand_documents": "social_midia_brand_documents",
    "automation_rules": "social_midia_automation_rules",
    "notifications": "social_midia_notifications",
    "agent_conversations": "social_midia_agent_conversations",
    "content_history": "social_midia_content_history",
    "brand_voice_profiles": "social_midia_brand_voice_profiles",
    "competitor_tracking": "social_midia_competitor_tracking",
}
