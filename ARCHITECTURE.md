# Tribus-AI — Architecture Reference
**Versão:** 1.0
**Atualizado em:** Abril 2026
**Mantido por:** PO (Jair)

> Este documento é leitura obrigatória antes de qualquer sessão de desenvolvimento.
> Claude Code deve ler este arquivo ANTES de ler qualquer outro arquivo do projeto.

---

## 1. Identidade do Projeto

Tribus-AI é um sistema RAG de inteligência tributária focado na Reforma Tributária
brasileira (EC 132/2023, LC 214/2025, LC 227/2026).

**Não é:** calculadora de tributos, ERP, gerador de obrigações acessórias.
**É:** sistema de apoio à decisão tributária com protocolo de 6 passos (P1→P6).

---

## 2. Raiz e Estrutura do Projeto

```
/Users/jairfahl/Downloads/tribus-ai-light/
├── auth.py                   ← Autenticação JWT + bcrypt
├── admin.py                  ← Painel admin (5 abas: Users/API/LegalHold/MAU/Onboarding)
├── ARCHITECTURE.md           ← Este arquivo
├── CLAUDE.md                 ← Regras e contexto permanente para Claude Code
├── landing/
│   └── index.html            ← Landing page pública (CTAs trial + WhatsApp)
├── ui/
│   ├── app.py                ← Entry point Streamlit + guard de sessão + onboarding
│   └── components/
│       ├── badge_criticidade.py      ← Badge 3 níveis: Crítico/Atenção/Informativo
│       ├── sugestoes_proativas.py    ← Sugestões de monitoramento de temas (G25)
│       ├── onboarding_profile.py     ← Progressive profiling 3 steps (GTM E)
│       ├── qualificacao_fatica.py    ← Qualificação fática do Eixo 3
│       ├── grau_consolidacao.py      ← Badge de grau de consolidação jurídica
│       └── saidas_stakeholder.py     ← Visões por público-alvo
├── pages/
│   └── login.py              ← Tela de login
├── components/
│   └── trial_banner.py       ← Banner de trial
├── src/
│   ├── api/
│   │   └── main.py           ← FastAPI — 19+ endpoints
│   ├── cognitive/
│   │   ├── engine.py         ← Orquestração cognitiva principal
│   │   ├── criticidade.py    ← Classificação de criticidade 3 níveis (G17)
│   │   ├── proatividade.py   ← Detecção de padrões + sugestões de monitoramento (G25)
│   │   ├── monitoramento_p6.py ← Ciclo pós-decisão P6 + verificação de premissas
│   │   └── aprendizado_institucional.py ← Extração de heurísticas de casos (G24)
│   ├── rag/
│   │   ├── retriever.py      ← Retrieval pgvector + adaptive tool chain
│   │   ├── hyde.py           ← HyDE — RDM-020
│   │   ├── multi_query.py    ← Multi-Query — RDM-024
│   │   ├── step_back.py      ← Step-Back — RDM-025
│   │   ├── corrector.py      ← CRAG
│   │   ├── adaptive.py       ← Adaptive retrieval chain
│   │   ├── ptf.py            ← PTF (Pre-retrieval Transformation)
│   │   ├── spd.py            ← SPD routing
│   │   ├── decomposer.py     ← Decomposição de queries
│   │   └── remissao_resolver.py ← RAR — Resolução Automática de Remissões
│   ├── billing/
│   │   ├── access.py         ← Controle de acesso por billing/trial
│   │   └── mau_tracker.py    ← Monthly Active Users — metering por análise (G26)
│   ├── integrity/
│   │   └── lockfile_manager.py ← Prompt Integrity — RDM-029
│   ├── outputs/              ← 5 classes de output acionável + legal_hold.py
│   ├── protocol/             ← Engine P1→P6
│   ├── quality/              ← Quality gate
│   ├── observability/        ← Métricas + drift + regression
│   ├── monitor/              ← Monitor de fontes oficiais
│   ├── ingest/               ← Pipeline de ingestão de PDFs
│   └── db/
│       └── pool.py           ← ThreadedConnectionPool — get_conn/put_conn (USAR SEMPRE)
├── migrations/
│   └── NNN_descricao.sql     ← Numeração sequencial obrigatória (última: 117)
└── tests/
    ├── unit/                 ← test_[modulo].py
    └── integration/          ← test_[fluxo].py
```

---

## 3. Stack — Tecnologias Ativas

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| API Backend | FastAPI (porta 8020) |
| Frontend | Streamlit (porta 8501) |
| Banco | PostgreSQL 16 + pgvector (HNSW, dim 1024) |
| Embeddings | Voyage-3 |
| LLM | Claude Sonnet 4.6 |
| Infraestrutura | Docker |
| Container DB | tribus-ai-db |
| DATABASE_URL | postgresql://taxmind:taxmind123@localhost:5436/taxmind_db |

**Tecnologias EXPLICITAMENTE EXCLUÍDAS (nunca usar):**
- LangChain
- LangGraph
- Supabase
- ChromaDB / FAISS / Pinecone

---

## 4. Responsabilidades dos Módulos

| Módulo | Responsabilidade | O que NÃO faz |
|---|---|---|
| `ui/app.py` | Entry point Streamlit, guard de sessão, onboarding, roteamento de abas | Zero lógica tributária, zero chamadas diretas ao banco |
| `src/cognitive/engine.py` | Orquestração do pipeline cognitivo completo | Zero renderização UI |
| `src/rag/retriever.py` | Retrieval HNSW, adaptive tool chain, PTF | Zero lógica de negócio tributária |
| `auth.py` | JWT, bcrypt, autenticação, busca de usuário | Zero renderização UI |
| `admin.py` | Renderização do painel admin (5 abas) | Zero lógica de negócio — delega a auth.py e queries diretas |
| `src/cognitive/criticidade.py` | Classifica Crítico/Atenção/Informativo por termos detectados | Zero renderização |
| `src/cognitive/proatividade.py` | Detecta padrões de tags e gera sugestões de monitoramento | Zero rendering |
| `src/cognitive/monitoramento_p6.py` | Ativa/encerra monitoramento P6, verifica premissas | Zero rendering |
| `src/cognitive/aprendizado_institucional.py` | Extrai heurísticas de casos encerrados, expira com 6 meses | Zero rendering |
| `src/billing/mau_tracker.py` | Registra e consulta MAU por análise realizada (DEC-08) | Zero lógica tributária |
| `src/outputs/legal_hold.py` | Ativa/desativa/verifica Legal Hold em outputs e interações | Zero rendering |
| `src/rag/remissao_resolver.py` | Resolve remissões entre normas e injeta no contexto (RAR) | Zero orquestração |
| `src/db/pool.py` | Pool de conexões psycopg2 — get_conn/put_conn | Zero lógica de negócio |
| `ui/components/onboarding_profile.py` | Progressive profiling 3 steps, persiste em users | Zero lógica tributária |
| `src/rag/hyde.py` | HyDE — geração de hipótese para expand de query | Zero orquestração |
| `src/rag/multi_query.py` | Multi-Query — variações paralelas da query | Zero orquestração |
| `src/rag/step_back.py` | Step-Back — query mais abstrata | Zero orquestração |
| `src/rag/corrector.py` | CRAG — verificação e correção do retrieval | Zero orquestração |
| `src/integrity/lockfile_manager.py` | Verificação de integridade de prompts (RDM-029) | Zero lógica tributária |
| `src/api/main.py` | Endpoints REST, validação de requests, serialização | Zero lógica de domínio — delega ao engine |

---

## 5. Pipeline Cognitivo — Ordem Obrigatória

```
PTF → Adaptive Params → SPD routing → Retrieve → CRAG →
  [Multi-Query > Step-Back > HyDE] (mutuamente exclusivos) →
  Quality Gate → Budget Manager (SUMMARY/FULL) → LLM
```

**Regra de exclusividade:** apenas UMA ferramenta RAG avançada por query.
Flag `_tool_activated` em `engine.py` controla isso. Nunca remover essa flag.

---

## 6. Protocolo de Decisão

**6 passos — imutável:**
- P1: Registrar & Classificar
- P2: Estruturar
- P3: Analisar
- P4: Hipotetizar
- P5: Decidir
- P6: Ciclo Pós-Decisão (Monitorar / Revisar / Aprender)

**P7, P8, P9 não existem.** Qualquer referência a eles é erro histórico da fase de design.

---

## 7. Regras Absolutas — Nunca Violar

### Segurança
- **Secrets via variável de ambiente.** Nunca hardcoded em código.
  - Correto: `os.getenv("JWT_SECRET", "fallback-apenas-dev")`
  - Errado: `JWT_SECRET = "minha-chave-secreta"`
- **Toda lógica de negócio e segurança: backend.** Streamlit captura intenção apenas.
- **Chamadas à Claude API: somente via engine.py.** Nunca do Streamlit diretamente.

### Banco de Dados
- **Toda nova feature que toca o banco começa por migration SQL versionada.**
  - Formato: `migrations/NNN_descricao.sql` (NNN = número sequencial de 3 dígitos)
  - Migration mais recente: `117_onboarding_profile.sql` → próxima será `118_...`
- **Nunca alterar schema sem migration.** ALTER TABLE direto no banco sem arquivo = proibido.

### Código
- **Nunca modificar um arquivo sem lê-lo completo primeiro.**
- **Nunca assumir o conteúdo de um arquivo — sempre ler.**
- **Novos módulos RAG:** criar em `src/rag/`, nunca dentro de `engine.py` diretamente.
- **Testes:** todo novo módulo tem `tests/unit/test_[modulo].py` correspondente.
- **Testes unitários:** NUNCA fazem chamadas externas (LLM, embeddings, banco real). Mockar sempre.

### Specs
- **Specs (.docx) nunca são editados diretamente.** Processo: unpack → editar XML → repack.
- **Nova versão de spec:** se v1.1 existe, a próxima é v1.2. Nunca sobrescrever.

### Gate de Qualidade
- **RDMs da Onda 1.5 estão implementados** (HyDE, Multi-Query, Step-Back, Context Budget, Lockfile). Não reimplementar.
- **597 testes devem passar** após qualquer modificação (referência pós GTM E, Abril 2026).
  - Comando: `pytest tests/ -v --tb=short`
  - 29 falhas pré-existentes DB são conhecidas e aceitáveis (requerem banco ativo)

---

## 8. Padrão de Isolamento por Feature

Antes de implementar qualquer feature, identificar e declarar:

```
Arquivos que serão CRIADOS: [lista explícita]
Arquivos que serão MODIFICADOS: [lista explícita + seção específica]
Arquivos que NÃO devem ser tocados: [lista explícita]
```

Se a implementação exigir tocar arquivo fora do escopo declarado: **parar e reportar ao PO**.

---

## 9. Corpus Tributário

**Normas na base (não subir via "Adicionar Norma"):**
- EC 132/2023
- LC 214/2025
- LC 227/2026

**"Adicionar Norma":** exclusivo para normas novas não presentes na base.

---

## 10. Histórico de Decisões Arquiteturais

| Decisão | Escolha | Motivo |
|---|---|---|
| GraphRAG | ❌ Excluído | Sem Gestor de Corpus para validar grafo |
| LangGraph | ❌ Excluído | Over-engineering para protocolo fixo |
| CRAG web fallback | ❌ Excluído | Base fechada |
| Supabase | ❌ Excluído | Docker na VPS é suficiente |
| ColBERT late interaction | 🔄 Candidato futuro | Reranking pós-HNSW — Onda 2+ |
| SLM híbrido | 🔄 Onda 3 | 3B–7B params para classificação/triage (DEC-09) |
| Protocolo 9→6 passos | ✅ Consolidado | P7/P8/P9 fundidos em P6 |
| Admin Module | ✅ Implementado | JWT + bcrypt + trial 30 dias + painel gestão (5 abas) |
| Pool de conexões unificado | ✅ Implementado | get_conn/put_conn em todos os módulos — sem _get_conn() local |
| Criticidade 3 níveis | ✅ Implementado | Crítico/Atenção/Informativo — G17, migration 114 |
| MAU Metering por análise | ✅ Implementado | DEC-08: usuário ativo = análise realizada, não login — G26, migration 115 |
| Proatividade customizada | ✅ Implementado | Detecção de padrões de tags, sugestões não intrusivas — G25, migration 116 |
| Onboarding progressive profiling | ✅ Implementado | 3 steps: step 0 obrigatório, 1-2 opcionais — GTM E, migration 117 |
| Landing page WhatsApp CTA | ✅ Implementado | Botão WhatsApp em hero + CTA final + footer — GTM A/DEC-11 |
| Badge "Memória de Decisão" | ✅ Implementado | Label no card do Dossiê na aba Documentos — GTM D |

---

## 11. Atualização deste Documento

Este documento deve ser atualizado sempre que:
- Um novo módulo for criado
- Uma decisão arquitetural for tomada ou revertida
- A estrutura de pastas mudar
- Uma regra absoluta for adicionada

**Quem atualiza:** PO (Jair) via este chat (Specs e Arquitetura).
**Como atualizar:** gerar prompt neste chat → executar no terminal.
