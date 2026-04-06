-- Migration: 0009_create_tenants
CREATE TABLE IF NOT EXISTS tenants (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    cnpj_raiz       VARCHAR(8)  NOT NULL UNIQUE,
    razao_social    VARCHAR(255) NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'suspended', 'canceled')),
    plano           VARCHAR(20) NOT NULL DEFAULT 'starter'
                    CHECK (plano IN ('starter', 'professional', 'enterprise')),
    config_json     JSONB       DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tenants_cnpj ON tenants (cnpj_raiz);

COMMENT ON TABLE tenants IS
    'Um tenant = um CNPJ raiz. Isolamento completo por tenant em todas as camadas.';
