BEGIN;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS tipo_atuacao      VARCHAR(20)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS cargo_responsavel VARCHAR(30)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS regime_tributario VARCHAR(20)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS faturamento_faixa VARCHAR(20)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS erp_utilizado     VARCHAR(100) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS dor_declarada     VARCHAR(280) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS onboarding_step   SMALLINT     DEFAULT 0;

COMMENT ON COLUMN users.tipo_atuacao IS
    'Qualificação de tenant — Insight E GTM Abril 2026';
COMMENT ON COLUMN users.onboarding_step IS
    '0=cadastro | 1=campos dia1-3 preenchidos | 2=campos dia7 preenchidos | 3=completo';

COMMIT;
