-- AgenteSocial - Schema Inicial
-- Migration 001: Tabelas principais

-- Habilitar extensoes
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Perfis de redes sociais conectados
-- ============================================
CREATE TABLE IF NOT EXISTS social_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  platform TEXT NOT NULL, -- instagram, youtube, tiktok, linkedin, twitter
  handle TEXT NOT NULL,
  platform_user_id TEXT,
  access_token TEXT, -- criptografado
  refresh_token TEXT,
  token_expires_at TIMESTAMPTZ,
  followers_count INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Pecas de conteudo geradas
-- ============================================
CREATE TABLE IF NOT EXISTS content_pieces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content_type TEXT NOT NULL, -- post, story, reel, carrossel, thread, video, podcast_script
  platform TEXT NOT NULL,
  title TEXT,
  body TEXT NOT NULL,
  caption TEXT,
  hashtags TEXT[] DEFAULT '{}',
  visual_suggestion TEXT,
  tone TEXT, -- formal, casual, humoristico, educativo, inspiracional
  status TEXT DEFAULT 'draft', -- draft, scheduled, published, archived
  engagement_score NUMERIC DEFAULT 0,
  posted_day TEXT, -- monday, tuesday, etc.
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Calendario editorial
-- ============================================
CREATE TABLE IF NOT EXISTS content_calendar (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content_id UUID REFERENCES content_pieces(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  platform TEXT NOT NULL,
  scheduled_at TIMESTAMPTZ NOT NULL,
  published_at TIMESTAMPTZ,
  status TEXT DEFAULT 'scheduled', -- scheduled, published, cancelled, failed
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Conteudo viral rastreado
-- ============================================
CREATE TABLE IF NOT EXISTS viral_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  platform TEXT NOT NULL,
  external_id TEXT, -- ID do post na plataforma
  author_handle TEXT,
  content_text TEXT,
  content_url TEXT,
  media_url TEXT,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  saves INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  virality_score NUMERIC DEFAULT 0,
  classification TEXT, -- normal, above_average, viral, super_viral
  niche TEXT,
  hashtags TEXT[] DEFAULT '{}',
  detected_at TIMESTAMPTZ DEFAULT now(),
  metadata JSONB DEFAULT '{}'
);

-- ============================================
-- Brand Voice (tom de voz da marca)
-- ============================================
CREATE TABLE IF NOT EXISTS brand_voice_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  tone TEXT, -- descricao do tom
  vocabulary TEXT[], -- palavras frequentes
  avoid_words TEXT[], -- palavras a evitar
  examples TEXT[], -- exemplos de textos
  personality TEXT, -- descricao da personalidade
  target_audience TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Hashtags pesquisadas
-- ============================================
CREATE TABLE IF NOT EXISTS hashtag_research (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  hashtag TEXT NOT NULL,
  platform TEXT NOT NULL,
  volume INTEGER,
  competition TEXT, -- low, medium, high
  related_hashtags TEXT[],
  trend_direction TEXT, -- up, stable, down
  niche TEXT,
  last_researched_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Podcasts e episodios
-- ============================================
CREATE TABLE IF NOT EXISTS podcast_episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  script TEXT,
  show_notes TEXT,
  topics TEXT[],
  audio_url TEXT,
  transcription TEXT,
  duration_seconds INTEGER,
  clips JSONB, -- [{start, end, title, description}]
  repurposed_content UUID[],
  status TEXT DEFAULT 'draft', -- draft, recorded, edited, published
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Relatorios gerados
-- ============================================
CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  type TEXT NOT NULL, -- weekly, monthly, quarterly, custom
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  data JSONB NOT NULL,
  pdf_url TEXT,
  sent_to TEXT[],
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Analytics snapshots
-- ============================================
CREATE TABLE IF NOT EXISTS analytics_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id UUID REFERENCES social_profiles(id) ON DELETE CASCADE,
  snapshot_date DATE NOT NULL,
  followers INTEGER,
  following INTEGER,
  posts_count INTEGER,
  engagement_rate NUMERIC,
  avg_likes NUMERIC,
  avg_comments NUMERIC,
  avg_shares NUMERIC,
  avg_views NUMERIC,
  top_performing_content JSONB,
  demographics JSONB,
  best_posting_times JSONB,
  metadata JSONB DEFAULT '{}'
);

-- ============================================
-- Documentos da marca (PDFs, manuais)
-- ============================================
CREATE TABLE IF NOT EXISTS brand_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type TEXT, -- brand_book, manual, reference, pdf
  content TEXT,
  file_url TEXT,
  embedding_ids TEXT[],
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Regras de automacao
-- ============================================
CREATE TABLE IF NOT EXISTS automation_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  trigger_type TEXT NOT NULL, -- schedule, event, trend_detected, date
  trigger_config JSONB NOT NULL,
  action_type TEXT NOT NULL, -- generate_content, send_report, send_email, notify
  action_config JSONB NOT NULL,
  is_active BOOLEAN DEFAULT true,
  last_triggered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Notificacoes
-- ============================================
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  channel TEXT NOT NULL, -- email, whatsapp, telegram, push, in_app
  type TEXT NOT NULL, -- report, alert, trend, summary
  subject TEXT,
  body TEXT,
  sent_at TIMESTAMPTZ,
  read_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'
);

-- ============================================
-- Conversas com agentes
-- ============================================
CREATE TABLE IF NOT EXISTS agent_conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT,
  agent_type TEXT,
  messages JSONB DEFAULT '[]',
  context JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Concorrentes rastreados
-- ============================================
CREATE TABLE IF NOT EXISTS competitor_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  platform TEXT NOT NULL,
  handle TEXT NOT NULL,
  name TEXT,
  followers_count INTEGER,
  engagement_rate NUMERIC,
  top_content JSONB,
  last_analyzed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Indexes
-- ============================================
CREATE INDEX IF NOT EXISTS idx_social_profiles_user ON social_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_content_pieces_user ON content_pieces(user_id);
CREATE INDEX IF NOT EXISTS idx_content_pieces_platform ON content_pieces(platform);
CREATE INDEX IF NOT EXISTS idx_content_calendar_user ON content_calendar(user_id);
CREATE INDEX IF NOT EXISTS idx_content_calendar_scheduled ON content_calendar(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_viral_content_score ON viral_content(virality_score DESC);
CREATE INDEX IF NOT EXISTS idx_viral_content_platform ON viral_content(platform);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_profile ON analytics_snapshots(profile_id);
CREATE INDEX IF NOT EXISTS idx_agent_conversations_user ON agent_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_user ON reports(user_id);

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_social_profiles_updated_at
  BEFORE UPDATE ON social_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_pieces_updated_at
  BEFORE UPDATE ON content_pieces
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_brand_voice_updated_at
  BEFORE UPDATE ON brand_voice_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_conversations_updated_at
  BEFORE UPDATE ON agent_conversations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
