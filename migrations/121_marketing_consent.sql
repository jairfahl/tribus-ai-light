-- Migration: 121_marketing_consent
-- Separa consentimento LGPD (obrigatório) de consentimento de marketing (opcional)
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS marketing_consent BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON COLUMN users.lgpd_consent       IS 'Aceite do tratamento de dados conforme LGPD (obrigatório para uso da plataforma)';
COMMENT ON COLUMN users.marketing_consent  IS 'Opt-in para receber comunicações de marketing (opcional)';
