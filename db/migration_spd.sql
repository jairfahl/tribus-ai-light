-- SPD-RAG: adiciona coluna retrieval_strategy a ai_interactions
ALTER TABLE ai_interactions ADD COLUMN IF NOT EXISTS retrieval_strategy VARCHAR(20) DEFAULT 'standard';
