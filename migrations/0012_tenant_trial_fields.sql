-- Migration: 0012_tenant_trial_fields
ALTER TABLE tenants
    ADD COLUMN IF NOT EXISTS trial_starts_at  TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS trial_ends_at    TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days'),
    ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'trial'
        CHECK (subscription_status IN ('trial', 'active', 'past_due', 'canceled'));

COMMENT ON COLUMN tenants.subscription_status IS
    'trial: dentro do período gratuito (7 dias)
     active: pagamento confirmado pela Vindi
     past_due: pagamento falhou, aguardando retry
     canceled: assinatura cancelada';
