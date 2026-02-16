-- AgenteSocial - RLS Policies
-- Migration 003: Row Level Security

-- ============================================
-- Habilitar RLS em todas as tabelas
-- ============================================
ALTER TABLE social_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_pieces ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_calendar ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_voice_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE hashtag_research ENABLE ROW LEVEL SECURITY;
ALTER TABLE podcast_episodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE automation_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitor_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_history ENABLE ROW LEVEL SECURITY;

-- viral_content e publico (leitura)

-- ============================================
-- Politicas: usuarios veem apenas seus dados
-- ============================================

-- Social Profiles
CREATE POLICY "Users can view own profiles"
  ON social_profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profiles"
  ON social_profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profiles"
  ON social_profiles FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profiles"
  ON social_profiles FOR DELETE
  USING (auth.uid() = user_id);

-- Content Pieces
CREATE POLICY "Users can view own content"
  ON content_pieces FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own content"
  ON content_pieces FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own content"
  ON content_pieces FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own content"
  ON content_pieces FOR DELETE
  USING (auth.uid() = user_id);

-- Content Calendar
CREATE POLICY "Users can manage own calendar"
  ON content_calendar FOR ALL
  USING (auth.uid() = user_id);

-- Brand Voice
CREATE POLICY "Users can manage own brand voice"
  ON brand_voice_profiles FOR ALL
  USING (auth.uid() = user_id);

-- Hashtag Research
CREATE POLICY "Users can manage own hashtag research"
  ON hashtag_research FOR ALL
  USING (auth.uid() = user_id);

-- Podcast Episodes
CREATE POLICY "Users can manage own podcasts"
  ON podcast_episodes FOR ALL
  USING (auth.uid() = user_id);

-- Reports
CREATE POLICY "Users can manage own reports"
  ON reports FOR ALL
  USING (auth.uid() = user_id);

-- Analytics Snapshots (via profile)
CREATE POLICY "Users can view own analytics"
  ON analytics_snapshots FOR SELECT
  USING (
    profile_id IN (
      SELECT id FROM social_profiles WHERE user_id = auth.uid()
    )
  );

-- Brand Documents
CREATE POLICY "Users can manage own documents"
  ON brand_documents FOR ALL
  USING (auth.uid() = user_id);

-- Automation Rules
CREATE POLICY "Users can manage own automations"
  ON automation_rules FOR ALL
  USING (auth.uid() = user_id);

-- Notifications
CREATE POLICY "Users can manage own notifications"
  ON notifications FOR ALL
  USING (auth.uid() = user_id);

-- Agent Conversations
CREATE POLICY "Users can manage own conversations"
  ON agent_conversations FOR ALL
  USING (auth.uid() = user_id);

-- Competitor Tracking
CREATE POLICY "Users can manage own competitors"
  ON competitor_tracking FOR ALL
  USING (auth.uid() = user_id);

-- Content History (Memory)
CREATE POLICY "Users can manage own memory"
  ON content_history FOR ALL
  USING (auth.uid() = user_id);

-- Viral Content (publico - somente leitura)
ALTER TABLE viral_content ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view viral content"
  ON viral_content FOR SELECT
  USING (true);

-- ============================================
-- Service role bypass (para o backend)
-- ============================================
-- O service_role_key do Supabase ja ignora RLS por padrao
