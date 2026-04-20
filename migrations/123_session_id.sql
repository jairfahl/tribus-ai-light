-- Migration: 123_session_id
-- Controle de sessão única por usuário (plano Starter = 1 user/1 sessão ativa)
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS session_id UUID DEFAULT gen_random_uuid();

UPDATE users SET session_id = gen_random_uuid() WHERE session_id IS NULL;

ALTER TABLE users ALTER COLUMN session_id SET NOT NULL;

CREATE INDEX IF NOT EXISTS idx_users_session_id ON users(session_id);
