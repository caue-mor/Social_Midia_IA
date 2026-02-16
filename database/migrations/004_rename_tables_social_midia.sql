-- AgenteSocial - Rename Tables to social_midia_ prefix
-- Migration 004: Distinguish from other projects in shared Supabase
-- Date: 2026-02-15

BEGIN;

-- ============================================================
-- 1. RENAME TABLES (15 tables)
-- ============================================================
ALTER TABLE IF EXISTS social_profiles RENAME TO social_midia_profiles;
ALTER TABLE IF EXISTS content_pieces RENAME TO social_midia_content_pieces;
ALTER TABLE IF EXISTS content_calendar RENAME TO social_midia_content_calendar;
ALTER TABLE IF EXISTS viral_content RENAME TO social_midia_viral_content;
ALTER TABLE IF EXISTS brand_voice_profiles RENAME TO social_midia_brand_voice_profiles;
ALTER TABLE IF EXISTS hashtag_research RENAME TO social_midia_hashtag_research;
ALTER TABLE IF EXISTS podcast_episodes RENAME TO social_midia_podcast_episodes;
ALTER TABLE IF EXISTS reports RENAME TO social_midia_reports;
ALTER TABLE IF EXISTS analytics_snapshots RENAME TO social_midia_analytics_snapshots;
ALTER TABLE IF EXISTS brand_documents RENAME TO social_midia_brand_documents;
ALTER TABLE IF EXISTS automation_rules RENAME TO social_midia_automation_rules;
ALTER TABLE IF EXISTS notifications RENAME TO social_midia_notifications;
ALTER TABLE IF EXISTS agent_conversations RENAME TO social_midia_agent_conversations;
ALTER TABLE IF EXISTS competitor_tracking RENAME TO social_midia_competitor_tracking;
ALTER TABLE IF EXISTS content_history RENAME TO social_midia_content_history;

-- ============================================================
-- 2. RENAME INDEXES
-- ============================================================
ALTER INDEX IF EXISTS idx_social_profiles_user RENAME TO idx_social_midia_profiles_user;
ALTER INDEX IF EXISTS idx_content_pieces_user RENAME TO idx_social_midia_content_pieces_user;
ALTER INDEX IF EXISTS idx_content_pieces_platform RENAME TO idx_social_midia_content_pieces_platform;
ALTER INDEX IF EXISTS idx_content_calendar_user RENAME TO idx_social_midia_content_calendar_user;
ALTER INDEX IF EXISTS idx_content_calendar_scheduled RENAME TO idx_social_midia_content_calendar_scheduled;
ALTER INDEX IF EXISTS idx_viral_content_score RENAME TO idx_social_midia_viral_content_score;
ALTER INDEX IF EXISTS idx_viral_content_platform RENAME TO idx_social_midia_viral_content_platform;
ALTER INDEX IF EXISTS idx_analytics_snapshots_profile RENAME TO idx_social_midia_analytics_snapshots_profile;
ALTER INDEX IF EXISTS idx_agent_conversations_user RENAME TO idx_social_midia_agent_conversations_user;
ALTER INDEX IF EXISTS idx_notifications_user RENAME TO idx_social_midia_notifications_user;
ALTER INDEX IF EXISTS idx_reports_user RENAME TO idx_social_midia_reports_user;
ALTER INDEX IF EXISTS idx_content_history_embedding RENAME TO idx_social_midia_content_history_embedding;
ALTER INDEX IF EXISTS idx_content_history_user RENAME TO idx_social_midia_content_history_user;

-- ============================================================
-- 3. RENAME TRIGGERS (drop and recreate with new names)
-- ============================================================
DROP TRIGGER IF EXISTS update_social_profiles_updated_at ON social_midia_profiles;
CREATE TRIGGER update_social_midia_profiles_updated_at
  BEFORE UPDATE ON social_midia_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_content_pieces_updated_at ON social_midia_content_pieces;
CREATE TRIGGER update_social_midia_content_pieces_updated_at
  BEFORE UPDATE ON social_midia_content_pieces
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_brand_voice_updated_at ON social_midia_brand_voice_profiles;
CREATE TRIGGER update_social_midia_brand_voice_updated_at
  BEFORE UPDATE ON social_midia_brand_voice_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_agent_conversations_updated_at ON social_midia_agent_conversations;
CREATE TRIGGER update_social_midia_agent_conversations_updated_at
  BEFORE UPDATE ON social_midia_agent_conversations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- 4. DROP OLD RLS POLICIES (they reference old table names internally)
-- ============================================================

-- social_midia_profiles (was social_profiles)
DROP POLICY IF EXISTS "Users can view own profiles" ON social_midia_profiles;
DROP POLICY IF EXISTS "Users can insert own profiles" ON social_midia_profiles;
DROP POLICY IF EXISTS "Users can update own profiles" ON social_midia_profiles;
DROP POLICY IF EXISTS "Users can delete own profiles" ON social_midia_profiles;

CREATE POLICY "social_midia_profiles_select" ON social_midia_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "social_midia_profiles_insert" ON social_midia_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "social_midia_profiles_update" ON social_midia_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "social_midia_profiles_delete" ON social_midia_profiles FOR DELETE USING (auth.uid() = user_id);

-- social_midia_content_pieces
DROP POLICY IF EXISTS "Users can view own content" ON social_midia_content_pieces;
DROP POLICY IF EXISTS "Users can insert own content" ON social_midia_content_pieces;
DROP POLICY IF EXISTS "Users can update own content" ON social_midia_content_pieces;
DROP POLICY IF EXISTS "Users can delete own content" ON social_midia_content_pieces;

CREATE POLICY "social_midia_content_pieces_all" ON social_midia_content_pieces FOR ALL USING (auth.uid() = user_id);

-- social_midia_content_calendar
DROP POLICY IF EXISTS "Users can manage own calendar" ON social_midia_content_calendar;
CREATE POLICY "social_midia_content_calendar_all" ON social_midia_content_calendar FOR ALL USING (auth.uid() = user_id);

-- social_midia_brand_voice_profiles
DROP POLICY IF EXISTS "Users can manage own brand voice" ON social_midia_brand_voice_profiles;
CREATE POLICY "social_midia_brand_voice_all" ON social_midia_brand_voice_profiles FOR ALL USING (auth.uid() = user_id);

-- social_midia_hashtag_research
DROP POLICY IF EXISTS "Users can manage own hashtag research" ON social_midia_hashtag_research;
CREATE POLICY "social_midia_hashtag_research_all" ON social_midia_hashtag_research FOR ALL USING (auth.uid() = user_id);

-- social_midia_podcast_episodes
DROP POLICY IF EXISTS "Users can manage own podcasts" ON social_midia_podcast_episodes;
CREATE POLICY "social_midia_podcast_episodes_all" ON social_midia_podcast_episodes FOR ALL USING (auth.uid() = user_id);

-- social_midia_reports
DROP POLICY IF EXISTS "Users can manage own reports" ON social_midia_reports;
CREATE POLICY "social_midia_reports_all" ON social_midia_reports FOR ALL USING (auth.uid() = user_id);

-- social_midia_analytics_snapshots
DROP POLICY IF EXISTS "Users can view own analytics" ON social_midia_analytics_snapshots;
CREATE POLICY "social_midia_analytics_snapshots_select" ON social_midia_analytics_snapshots FOR SELECT
  USING (profile_id IN (SELECT id FROM social_midia_profiles WHERE user_id = auth.uid()));

-- social_midia_brand_documents
DROP POLICY IF EXISTS "Users can manage own documents" ON social_midia_brand_documents;
CREATE POLICY "social_midia_brand_documents_all" ON social_midia_brand_documents FOR ALL USING (auth.uid() = user_id);

-- social_midia_automation_rules
DROP POLICY IF EXISTS "Users can manage own automations" ON social_midia_automation_rules;
CREATE POLICY "social_midia_automation_rules_all" ON social_midia_automation_rules FOR ALL USING (auth.uid() = user_id);

-- social_midia_notifications
DROP POLICY IF EXISTS "Users can manage own notifications" ON social_midia_notifications;
CREATE POLICY "social_midia_notifications_all" ON social_midia_notifications FOR ALL USING (auth.uid() = user_id);

-- social_midia_agent_conversations
DROP POLICY IF EXISTS "Users can manage own conversations" ON social_midia_agent_conversations;
CREATE POLICY "social_midia_agent_conversations_all" ON social_midia_agent_conversations FOR ALL USING (auth.uid() = user_id);

-- social_midia_competitor_tracking
DROP POLICY IF EXISTS "Users can manage own competitors" ON social_midia_competitor_tracking;
CREATE POLICY "social_midia_competitor_tracking_all" ON social_midia_competitor_tracking FOR ALL USING (auth.uid() = user_id);

-- social_midia_content_history
DROP POLICY IF EXISTS "Users can manage own memory" ON social_midia_content_history;
CREATE POLICY "social_midia_content_history_all" ON social_midia_content_history FOR ALL USING (auth.uid() = user_id);

-- social_midia_viral_content (public read)
DROP POLICY IF EXISTS "Anyone can view viral content" ON social_midia_viral_content;
CREATE POLICY "social_midia_viral_content_select" ON social_midia_viral_content FOR SELECT USING (true);

COMMIT;
