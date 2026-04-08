-- Migration 106: campos de qualificação fática em ai_interactions.
--
-- G23: Qualificação Fática Estruturada (DC v7, Eixo 3).
-- Registra os fatos do cliente e o semáforo de completude para rastreabilidade
-- e análise da qualidade das consultas (analytics de completude).
--
BEGIN;

ALTER TABLE ai_interactions
    ADD COLUMN IF NOT EXISTS qf_cnae_principal    VARCHAR(50)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS qf_regime_tributario VARCHAR(30)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS qf_ufs_operacao      TEXT         DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS qf_tipo_operacao     VARCHAR(20)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS qf_faturamento_faixa VARCHAR(40)  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS qf_semaforo          VARCHAR(10)  DEFAULT NULL;

COMMENT ON COLUMN ai_interactions.qf_cnae_principal IS
    'CNAE principal da empresa informado na qualificação fática (G23)';
COMMENT ON COLUMN ai_interactions.qf_regime_tributario IS
    'Regime tributário da empresa: Lucro Real | Lucro Presumido | Simples Nacional | MEI';
COMMENT ON COLUMN ai_interactions.qf_ufs_operacao IS
    'Estados de operação da empresa (origem e destino)';
COMMENT ON COLUMN ai_interactions.qf_tipo_operacao IS
    'Tipo de operação predominante: B2B | B2C | Intragrupo | Exportação | Misto';
COMMENT ON COLUMN ai_interactions.qf_faturamento_faixa IS
    'Faixa de faturamento bruto anual da empresa';
COMMENT ON COLUMN ai_interactions.qf_semaforo IS
    'Semáforo de completude fática: verde | amarelo | vermelho (G23)';

COMMIT;

-- Verificação pós-migration
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'ai_interactions' AND column_name = 'qf_semaforo'
    ) THEN
        RAISE EXCEPTION 'Migration 106 falhou: coluna qf_semaforo não encontrada.';
    END IF;
    RAISE NOTICE 'Migration 106 aplicada com sucesso.';
END;
$$;
