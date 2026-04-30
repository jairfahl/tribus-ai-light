-- Migration 132: adiciona cpf_cnpj ao tenant para validação Asaas na assinatura
-- CPF (11 dígitos) ou CNPJ (14 dígitos) do responsável / empresa.
-- Obrigatório apenas no ato da assinatura (validado pelo Asaas).

ALTER TABLE tenants
  ADD COLUMN IF NOT EXISTS cpf_cnpj VARCHAR(18);
