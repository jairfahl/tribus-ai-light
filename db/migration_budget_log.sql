-- Context Budget Log: pressão de contexto por análise
-- context_budget_log já adicionado por migration_progressive_loading.sql
ALTER TABLE ai_interactions
  ADD COLUMN IF NOT EXISTS budget_pressao_pct DECIMAL(5,2);
