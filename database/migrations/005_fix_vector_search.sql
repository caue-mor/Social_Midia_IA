-- AgenteSocial - Fix Vector Search Functions
-- Migration 005: Update match_content functions to use social_midia_content_history

-- Drop old functions
DROP FUNCTION IF EXISTS match_content(TEXT, INTEGER, UUID);
DROP FUNCTION IF EXISTS match_content_by_embedding(vector, INTEGER, UUID, FLOAT);

-- Recreate match_content with new table name
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
BEGIN
  RETURN QUERY
  SELECT
    ch.id,
    ch.content,
    ch.content_type,
    1.0::FLOAT AS similarity,
    ch.metadata,
    ch.created_at
  FROM social_midia_content_history ch
  WHERE (filter_user_id IS NULL OR ch.user_id = filter_user_id)
    AND ch.content ILIKE '%' || query_text || '%'
  ORDER BY ch.created_at DESC
  LIMIT match_count;
END;
$$;

-- Recreate match_content_by_embedding with new table name
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
  FROM social_midia_content_history ch
  WHERE (filter_user_id IS NULL OR ch.user_id = filter_user_id)
    AND ch.embedding IS NOT NULL
    AND (1 - (ch.embedding <=> query_embedding)) >= similarity_threshold
  ORDER BY ch.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
