-- Migration 103: campos premissas, riscos_fiscais e p2_concluido em ai_interactions.
--
-- G02: P2 do Protocolo de Decisão requer declaração explícita de
-- premissas regulatórias (mín. 3) e riscos fiscais (mín. 3) antes de
-- qualquer análise de IA. Esses campos persistem as declarações do gestor
-- para auditoria, retroalimentação e análise de qualidade.
--
BEGIN;

ALTER TABLE ai_interactions
    ADD COLUMN IF NOT EXISTS premissas      TEXT[]  DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS riscos_fiscais TEXT[]  DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS p2_concluido   BOOLEAN DEFAULT FALSE;

COMMENT ON COLUMN ai_interactions.premissas IS
    'Premissas regulatórias declaradas no P2 (mín. 3)';
COMMENT ON COLUMN ai_interactions.riscos_fiscais IS
    'Riscos fiscais declarados no P2 (mín. 3)';
COMMENT ON COLUMN ai_interactions.p2_concluido IS
    'Flag: P2 foi concluído com os mínimos obrigatórios (>= 3 premissas e >= 3 riscos)';

COMMIT;

-- Verificação pós-migration
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'ai_interactions' AND column_name = 'premissas'
    ) THEN
        RAISE EXCEPTION 'Migration 103 falhou: coluna premissas não encontrada.';
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'ai_interactions' AND column_name = 'riscos_fiscais'
    ) THEN
        RAISE EXCEPTION 'Migration 103 falhou: coluna riscos_fiscais não encontrada.';
    END IF;
    RAISE NOTICE 'Migration 103 aplicada com sucesso.';
END;
$$;
