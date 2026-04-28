-- Migration 130: tabela persistente para jobs de ingestão
-- Substitui o dict em memória _ingest_jobs, permitindo múltiplos workers.

CREATE TABLE IF NOT EXISTS ingest_jobs (
    job_id      UUID        PRIMARY KEY,
    status      TEXT        NOT NULL DEFAULT 'pending',
    message     TEXT        NOT NULL DEFAULT '',
    result      JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ingest_jobs_created_at ON ingest_jobs (created_at DESC);
