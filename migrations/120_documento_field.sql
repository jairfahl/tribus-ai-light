-- Migration: 120_documento_field
-- Alarga cnpj_raiz para suportar CPF (11 dígitos) e CNPJ completo (14 dígitos)
ALTER TABLE tenants
  ALTER COLUMN cnpj_raiz TYPE VARCHAR(18);
