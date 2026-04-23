-- migrations/127_churn_email_tracking.sql
-- Rastreamento de e-mails de retenção + motivo de cancelamento
-- Gerado em: 2026-04-23

ALTER TABLE tenants
  ADD COLUMN IF NOT EXISTS trial_d3_email_sent_at   TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS trial_d1_email_sent_at   TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS inactivity_email_sent_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS cancel_reason            TEXT;

COMMENT ON COLUMN tenants.trial_d3_email_sent_at   IS 'Quando o e-mail de aviso D-3 do trial foi enviado';
COMMENT ON COLUMN tenants.trial_d1_email_sent_at   IS 'Quando o e-mail de aviso D-1 do trial foi enviado';
COMMENT ON COLUMN tenants.inactivity_email_sent_at IS 'Quando o e-mail de inatividade (14 dias) foi enviado; NULL = elegível para envio';
COMMENT ON COLUMN tenants.cancel_reason            IS 'Motivo de cancelamento coletado no exit survey';
