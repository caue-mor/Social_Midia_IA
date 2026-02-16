-- AgenteSocial - Memory Tables
-- Migration 002: Tabelas de memoria (pgvector + RAG)

-- Habilitar pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- Historico de conteudo (Memoria Episodica)
-- ============================================
CREATE TABLE IF NOT EXISTS content_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  content_type TEXT, -- post, insight, feedback, learning
  embedding vector(1536), -- OpenAI text-embedding-3-small
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Index para busca vetorial
CREATE INDEX IF NOT EXISTS idx_content_history_embedding
  ON content_history USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_content_history_user
  ON content_history(user_id);

-- ============================================
-- Funcao de busca semantica (match_content)
-- ============================================
CREATE OR REPLACE FUNCTION match_content(
  query_text TEXT,
  match_count INTEGER DEFAULT 10,
  filter_user_id UUID DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  content_type TEXT,
  similarity FLOAT,
  metadata JSONB,
  created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
DECLARE
  query_embedding vector(1536);
BEGIN
  -- Gera embedding via pg_net (ou pre-calculado via API)
  -- Por enquanto, usa busca por texto simples como fallback
  -- Na producao, o embedding e calculado pela API antes de chamar esta funcao
  RETURN QUERY
  SELECT
    ch.id,
    ch.content,
    ch.content_type,
    1.0::FLOAT AS similarity,
    ch.metadata,
    ch.created_at
  FROM content_history ch
  WHERE (filter_user_id IS NULL OR ch.user_id = filter_user_id)
    AND ch.content ILIKE '%' || query_text || '%'
  ORDER BY ch.created_at DESC
  LIMIT match_count;
END;
$$;

-- ============================================
-- Funcao de busca por embedding (producao)
-- ============================================
CREATE OR REPLACE FUNCTION match_content_by_embedding(
  query_embedding vector(1536),
  match_count INTEGER DEFAULT 10,
  filter_user_id UUID DEFAULT NULL,
  similarity_threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  content_type TEXT,
  similarity FLOAT,
  metadata JSONB,
  created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    ch.id,
    ch.content,
    ch.content_type,
    (1 - (ch.embedding <=> query_embedding))::FLOAT AS similarity,
    ch.metadata,
    ch.created_at
  FROM content_history ch
  WHERE (filter_user_id IS NULL OR ch.user_id = filter_user_id)
    AND (1 - (ch.embedding <=> query_embedding)) >= similarity_threshold
  ORDER BY ch.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
