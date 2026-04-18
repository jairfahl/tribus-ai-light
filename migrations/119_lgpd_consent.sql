-- Migration: 119_lgpd_consent
-- Adiciona campos LGPD e verificação de e-mail à tabela users

ALTER TABLE users
  ADD COLUMN IF NOT EXISTS lgpd_consent      BOOLEAN     NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS lgpd_consent_at   TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS email_verificado  BOOLEAN     NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS email_token       VARCHAR(64);

COMMENT ON COLUMN users.lgpd_consent    IS 'Consentimento LGPD para comunicações de marketing';
COMMENT ON COLUMN users.lgpd_consent_at IS 'Timestamp do aceite LGPD';
COMMENT ON COLUMN users.email_verificado IS 'E-mail confirmado via link de verificação';
COMMENT ON COLUMN users.email_token      IS 'Token UUID para verificação de e-mail; NULL após confirmado';

CREATE INDEX IF NOT EXISTS idx_users_email_token
  ON users(email_token)
  WHERE email_token IS NOT NULL;

-- Usuários já existentes têm e-mail implicitamente verificado (criados pelo admin)
UPDATE users SET email_verificado = TRUE WHERE email_verificado = FALSE;
