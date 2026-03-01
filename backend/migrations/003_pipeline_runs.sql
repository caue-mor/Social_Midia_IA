-- Pipeline runs: armazena execucoes do pipeline de conteudo
CREATE TABLE IF NOT EXISTS social_midia_pipeline_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    version INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed')),
    config JSONB DEFAULT '{}',
    audit_result JSONB,
    plan_result JSONB,
    content_results JSONB,
    quality_report JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    completed_at TIMESTAMPTZ,
    UNIQUE(user_id, version)
);

ALTER TABLE social_midia_pipeline_runs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users see own pipeline runs"
    ON social_midia_pipeline_runs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users insert own pipeline runs"
    ON social_midia_pipeline_runs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users update own pipeline runs"
    ON social_midia_pipeline_runs FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Service role full access"
    ON social_midia_pipeline_runs FOR ALL
    USING (auth.role() = 'service_role');
