-- Migration: 025_step_back_fields.sql
-- Step-Back Prompting (RDM-025)
ALTER TABLE ai_interactions
  ADD COLUMN IF NOT EXISTS step_back_activated    BOOLEAN  DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS step_back_query        TEXT     DEFAULT NULL;
