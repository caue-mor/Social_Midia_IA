-- ============================================
-- Migration 006: AGNO 2.5.2 — Schema 'ai'
-- ============================================
-- O AGNO 2.5.2 auto-cria as tabelas no schema 'ai' quando
-- create_schema=True (default no PostgresDb).
--
-- Tabelas criadas automaticamente pelo AGNO:
--   ai.agno_sessions     — sessoes de Agent, Team, Workflow
--   ai.agno_memories     — memorias de usuario
--   ai.agno_schema_versions — controle de versao de schema
--   (+ metrics, eval_runs, knowledge, traces, spans, etc. sob demanda)
--
-- Esta migration apenas garante que:
-- 1. O schema 'ai' existe
-- 2. RLS esta habilitado nas tabelas AGNO
-- 3. Indices extras para performance
-- ============================================

-- 1. Garante que o schema 'ai' existe
CREATE SCHEMA IF NOT EXISTS ai;

-- 2. Habilita RLS nas tabelas AGNO (seguranca Supabase)
DO $$
BEGIN
    -- agno_sessions
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'ai' AND table_name = 'agno_sessions') THEN
        ALTER TABLE ai.agno_sessions ENABLE ROW LEVEL SECURITY;
    END IF;

    -- agno_memories
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'ai' AND table_name = 'agno_memories') THEN
        ALTER TABLE ai.agno_memories ENABLE ROW LEVEL SECURITY;
    END IF;
END
$$;

-- 3. Policies para acesso service_role (backend)
DO $$
BEGIN
    -- Sessions: service_role tem acesso total
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE schemaname = 'ai' AND tablename = 'agno_sessions' AND policyname = 'service_role_all_sessions') THEN
        CREATE POLICY service_role_all_sessions ON ai.agno_sessions
            FOR ALL
            USING (current_setting('role') = 'service_role')
            WITH CHECK (current_setting('role') = 'service_role');
    END IF;

    -- Memories: service_role tem acesso total
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE schemaname = 'ai' AND tablename = 'agno_memories' AND policyname = 'service_role_all_memories') THEN
        CREATE POLICY service_role_all_memories ON ai.agno_memories
            FOR ALL
            USING (current_setting('role') = 'service_role')
            WITH CHECK (current_setting('role') = 'service_role');
    END IF;
END
$$;

-- 4. Indices extras para performance de queries por user_id
CREATE INDEX IF NOT EXISTS idx_agno_sessions_user_id
    ON ai.agno_sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_agno_memories_user_id
    ON ai.agno_memories(user_id);

CREATE INDEX IF NOT EXISTS idx_agno_sessions_session_type
    ON ai.agno_sessions(session_type);
