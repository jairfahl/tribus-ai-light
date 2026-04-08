BEGIN;

-- Padrões de uso detectados por usuário
CREATE TABLE IF NOT EXISTS padroes_uso (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID        NOT NULL REFERENCES users(id),
    tema            VARCHAR(50) NOT NULL,
    contagem        INT         NOT NULL DEFAULT 1,
    primeira_vez    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ultima_vez      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sugestao_ativa  BOOLEAN     NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_padrao_user_tema UNIQUE (user_id, tema)
);

CREATE INDEX IF NOT EXISTS idx_padroes_user ON padroes_uso (user_id);
CREATE INDEX IF NOT EXISTS idx_padroes_tema ON padroes_uso (tema);

-- Silenciamentos de sugestões
CREATE TABLE IF NOT EXISTS sugestoes_silenciadas (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID        NOT NULL REFERENCES users(id),
    tema            VARCHAR(50) NOT NULL,
    silenciado_ate  DATE        NOT NULL,
    criado_em       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_silencio_user_tema UNIQUE (user_id, tema)
);

CREATE INDEX IF NOT EXISTS idx_silencio_user ON sugestoes_silenciadas (user_id);

COMMIT;
