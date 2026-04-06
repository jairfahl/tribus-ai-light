-- Migration: 0013_tenant_asaas_fields
ALTER TABLE tenants
    ADD COLUMN IF NOT EXISTS asaas_customer_id     VARCHAR(100),
    ADD COLUMN IF NOT EXISTS asaas_subscription_id VARCHAR(100);

COMMENT ON COLUMN tenants.asaas_customer_id     IS 'ID do customer no Asaas';
COMMENT ON COLUMN tenants.asaas_subscription_id IS 'ID da subscription no Asaas';
