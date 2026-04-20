-- Migration: 124_tenant_desconto
-- Permite admin conceder desconto percentual por tenant antes da assinatura Asaas
ALTER TABLE tenants
  ADD COLUMN IF NOT EXISTS desconto_percentual NUMERIC(5,2) NOT NULL DEFAULT 0
    CHECK (desconto_percentual >= 0 AND desconto_percentual <= 100);

COMMENT ON COLUMN tenants.desconto_percentual IS
  'Desconto percentual concedido pelo admin (0–100). Aplicado na criação da assinatura Asaas.';
