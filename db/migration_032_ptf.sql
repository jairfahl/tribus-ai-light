-- Migration: 032_ptf_fields.sql
-- Pre-filter Temporal (PTF) — campos de vigência em chunks e observabilidade em ai_interactions

-- 1. Campos de vigência na tabela chunks
ALTER TABLE chunks
  ADD COLUMN IF NOT EXISTS vigencia_inicio DATE,
  ADD COLUMN IF NOT EXISTS vigencia_fim    DATE,
  ADD COLUMN IF NOT EXISTS regime          VARCHAR(20)
    CHECK (regime IN ('vigente', 'transicao', 'definitivo'));

-- 2. Índice para acelerar WHERE temporal
CREATE INDEX IF NOT EXISTS idx_chunks_vigencia
  ON chunks (vigencia_inicio, vigencia_fim);

CREATE INDEX IF NOT EXISTS idx_chunks_regime
  ON chunks (regime);

-- 3. Campos de observabilidade PTF em ai_interactions
ALTER TABLE ai_interactions
  ADD COLUMN IF NOT EXISTS data_referencia_utilizado DATE,
  ADD COLUMN IF NOT EXISTS is_future_scenario        BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS chunks_pre_filtro         INTEGER,
  ADD COLUMN IF NOT EXISTS chunks_pos_filtro         INTEGER;

-- 4. Popular regime nos chunks existentes
-- EC 132/2023, LC 214/2025 e LC 227/2026 cobrem transição E definitivo.
-- Como não há campo artigo-por-artigo que distinga regimes, marcamos os chunks
-- dessas normas como abrangendo ambos os períodos (transição + definitivo).
-- O PTF vai incluí-los em qualquer busca de 2027+.
-- Chunks de normas tipo "Outro" (uploads manuais) ficam sem regime (sempre incluídos).

-- Normas base (EC/LC): cobrem transição e definitivo
UPDATE chunks
SET vigencia_inicio = '2024-01-01',
    vigencia_fim    = '9999-12-31',
    regime          = NULL
WHERE norma_id IN (
  SELECT id FROM normas WHERE tipo IN ('EC', 'LC')
)
AND regime IS NULL;

-- Normas de tipo IN/Resolução/Parecer/Manual: regime vigente por padrão
UPDATE chunks
SET vigencia_inicio = '2024-01-01',
    vigencia_fim    = '2026-12-31',
    regime          = 'vigente'
WHERE norma_id IN (
  SELECT id FROM normas WHERE tipo IN ('IN', 'Resolução', 'Parecer', 'Manual')
)
AND regime IS NULL;
