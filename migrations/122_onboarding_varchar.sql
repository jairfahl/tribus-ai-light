-- Migration: 122_onboarding_varchar
-- Alarga campos de onboarding que estouravam VARCHAR(20) com labels reais do frontend
ALTER TABLE users
  ALTER COLUMN tipo_atuacao      TYPE VARCHAR(100),
  ALTER COLUMN regime_tributario TYPE VARCHAR(100),
  ALTER COLUMN faturamento_faixa TYPE VARCHAR(100);
