-- Monitor de fontes oficiais — detecta novos documentos legislativos
CREATE TABLE IF NOT EXISTS monitor_fontes (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(100)  NOT NULL,
    url             VARCHAR(500)  NOT NULL,
    tipo_fonte      VARCHAR(30)   NOT NULL,  -- 'dou' | 'planalto' | 'cgibs' | 'nfe' | 'rfb'
    ativo           BOOLEAN       DEFAULT TRUE,
    ultimo_check    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ   DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS monitor_documentos (
    id              SERIAL PRIMARY KEY,
    fonte_id        INTEGER       REFERENCES monitor_fontes(id),
    titulo          VARCHAR(500)  NOT NULL,
    url             VARCHAR(1000),
    data_publicacao VARCHAR(30),
    resumo          TEXT,
    status          VARCHAR(20)   DEFAULT 'novo',  -- 'novo' | 'ingerido' | 'descartado'
    detectado_em    TIMESTAMPTZ   DEFAULT NOW(),
    atualizado_em   TIMESTAMPTZ   DEFAULT NOW(),
    UNIQUE(url)
);

-- Fontes pre-configuradas
INSERT INTO monitor_fontes (nome, url, tipo_fonte) VALUES
    ('DOU - Reforma Tributária', 'https://www.in.gov.br/consulta/-/buscar/dou?q=reforma+tribut%C3%A1ria&s=todos&exactDate=dia&sortType=0', 'dou'),
    ('Planalto - Leis Complementares', 'https://www.planalto.gov.br/ccivil_03/leis/lcp/', 'planalto'),
    ('CGIBS - Orientações', 'https://www.gov.br/cgibs/', 'cgibs'),
    ('Portal NF-e - Notas Técnicas', 'https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=tW+YMyk/50s=', 'nfe'),
    ('Receita Federal - Legislação', 'https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/legislacao', 'rfb')
ON CONFLICT DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_monitor_docs_status ON monitor_documentos (status);
