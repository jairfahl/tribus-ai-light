-- Migration 130: Adiciona expiração do token de verificação de e-mail
-- Tokens sem data de expiração (registros antigos) continuam válidos (IS NULL = sem expiração).
-- Novos registros recebem email_token_expires_at = NOW() + INTERVAL '24 hours'.

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS email_token_expires_at TIMESTAMPTZ;
