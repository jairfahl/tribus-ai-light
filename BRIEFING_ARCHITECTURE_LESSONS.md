# Briefing — ARCHITECTURE.md e LESSONS_LEARNED.md
**Para:** Novo projeto que adota este modelo de documentação
**Contexto:** Padrão desenvolvido e refinado no Orbis.tax ao longo de múltiplos sprints
  com operação solo (1 PO + Claude Code como engineer)

---

## O que são esses dois arquivos

São documentos vivos que substituem a memória da equipe. Num time grande, parte do contexto
fica na cabeça das pessoas. Numa operação solo com IA como co-engineer, esse contexto precisa
estar escrito — porque a IA começa do zero a cada sessão.

Eles não se duplicam. Têm responsabilidades distintas:

| Documento | Responde a | Tom | Frequência de leitura |
|---|---|---|---|
| `ARCHITECTURE.md` | "Como o sistema está estruturado e quais são as regras permanentes?" | Técnico, prescritivo | Toda sessão de dev |
| `LESSONS_LEARNED.md` | "Por que as regras existem? O que custou não segui-las?" | Narrativo, causal | Antes de decisão relevante ou deploy |

---

## ARCHITECTURE.md

### Para que serve

É o mapa do sistema. Qualquer pessoa (ou IA) que ler este arquivo deve ser capaz de
responder, sem abrir código:

- Quais tecnologias estão em uso e quais são explicitamente proibidas
- Quais módulos existem e o que cada um faz (e o que **não** faz)
- Quais regras absolutas nunca podem ser violadas
- Qual é o histórico de decisões arquiteturais e por que foram tomadas
- Qual é o estado atual das entregas

### Quando é usado

- **Início de toda sessão de desenvolvimento** — leitura obrigatória antes de escrever qualquer linha
- **Antes de propor uma nova feature** — para verificar se colide com decisão já tomada
- **Antes de qualquer migration de banco** — para consultar numeração, convenções, tabelas existentes
- **Onboarding de novo colaborador** — substitui semanas de "pair programming para entender o sistema"
- **Antes de qualquer deploy** — para confirmar que nada saiu do escopo declarado

### O que ele contém (estrutura recomendada)

```
1. Identidade do projeto — o que é, o que não é
2. Estrutura de pastas anotada — com propósito de cada arquivo relevante
3. Stack ativa — o que usar e o que nunca usar (lista explícita)
4. Responsabilidades dos módulos — o que cada módulo faz e o que ele não faz
5. Pipeline/fluxo principal — ordem obrigatória de operações
6. Regras absolutas — segurança, banco, código, deploy
7. Padrão de isolamento por feature — escopo declarado antes de codar
8. Histórico de decisões arquiteturais — tabela com decisão, escolha e motivo
9. Instrução de atualização — quando e como manter o documento
```

### Benefícios mensuráveis

**Redução de retrabalho.** Toda vez que uma feature foi implementada sem ler o ARCHITECTURE.md,
houve colisão com decisão já tomada. Retrabalho de 1–3 sessões por incidente.

**Aceleração de onboarding.** Um colaborador novo (humano ou IA) que lê o arquivo completo
opera com contexto equivalente a semanas de imersão no código.

**Prevenção de "redescoberta".** Sem o histórico de decisões, a mesma discussão
(LangChain sim/não, PostgreSQL vs. Supabase, protocolo com 6 ou 9 passos) se repete a cada ciclo.
O histórico encerra o debate com evidência, não com opinião.

**Segurança como documentação.** Regras como "nunca hardcode secrets", "sempre usar pool de
conexões", "VARCHAR larga o suficiente para o label mais longo da UI" estão no arquivo —
não dependem da memória de ninguém.

### Como manter

Atualizar imediatamente quando:
- Um novo módulo é criado
- Uma decisão arquitetural é tomada (mesmo que seja "descartamos X")
- Uma regra absoluta é adicionada
- A estrutura de pastas muda
- O estado de uma entrega muda (⏳ → ✅)
- A última migration muda

**Quem atualiza:** o PO, ao final de cada sessão de entrega.
**Tempo médio:** 5–10 minutos por atualização incremental.

---

## LESSONS_LEARNED.md

### Para que serve

Captura o **custo real** dos erros e as regras que derivaram deles. Não é um log de bugs —
é um documento de inteligência operacional. A diferença:

- Log de bug: "migration 122 não estava aplicada em prod"
- Lição aprendida: "declarar ✅ sem evidência empírica é risco real — sempre verificar
  com `information_schema.columns` antes de registrar migration como aplicada"

A lição é acionável em qualquer projeto futuro. O log de bug, não.

### Quando é usado

- **Antes de qualquer deploy em produção** — para não repetir os erros de deploy anteriores
- **Antes de decisão arquitetural nova** — para verificar se já houve custo relacionado
- **Ao investigar um bug** — para checar se existe lição prévia que direcione o diagnóstico
- **Ao iniciar nova feature com banco** — para consultar lições de migration e schema
- **Revisão mensal** — para fechar débitos abertos e atualizar status

### O que ele contém (estrutura recomendada)

```
1. Governança de produto — o que funciona, o que causou problemas
2. Governança do corpus (se houver base de conhecimento)
3. Arquitetura e engenharia — padrões que funcionam + erros que custaram caro
4. Deploy e infraestrutura — armadilhas de ambiente, containers, variáveis
5. DNS e domínio (se aplicável)
6. Debugging e diagnóstico — ordem correta de investigação
7. Processo de trabalho com IA — o que acelera, o que cria ruído
8. Segurança — o que funciona, o que foi postergado e custou
9. Decisões que não devem ser questionadas novamente
10. Débitos abertos — com risco e gatilho para resolver
```

### Benefícios mensuráveis

**Memória institucional que não depende de pessoa.** Em operação solo, o único repositório
de "por que fizemos assim" é este arquivo. Sem ele, cada sessão começa do zero.

**Redução de tempo de diagnóstico.** A lição "ao investigar falha silenciosa em PATCH,
verificar schema das colunas no banco antes do código" teria economizado 2+ horas
de rastreamento no caso do OnboardingModal travado.

**Prevenção de repetição de erros custosos.** Erros como "docker restart não relê env_file",
"DKIM TXT acima de 255 chars precisa ser dividido", "APP_URL pode ser corrompida por
colagem de dois comandos na mesma linha" não têm custo técnico de evitar —
têm custo altíssimo de redescobrir.

**Clareza sobre débitos reais.** A seção de débitos abertos separa o que é risco crescente
(D-03: IDs sequenciais, D-07: staging inexistente) do que foi fechado (D-01: BYPASS_AUTH,
D-02: backup). Sem isso, "o que está pendente" é julgamento subjetivo.

### Como manter

Adicionar entrada imediatamente após:
- Qualquer incidente de produção (mesmo que resolvido em minutos)
- Qualquer bug que levou mais de 30 minutos para diagnosticar
- Qualquer decisão que foi tomada com análise formal
- Qualquer débito fechado (marcar ✅ com data)

Formato de nova entrada:
```markdown
**[Título curto e direto]**
[O que aconteceu — 2 a 4 linhas]
**Regra derivada:** [o que fazer diferente da próxima vez — acionável]
```

**Quem atualiza:** o PO, no momento do incidente ou imediatamente após.
**Tempo médio:** 5 minutos por entrada. O custo de não registrar é ordens de magnitude maior.

---

## Como adotar em um novo projeto

### Fase 1 — Bootstrap (semana 1)

1. Criar `ARCHITECTURE.md` com as seções 1–4 preenchidas (identidade, stack, estrutura, módulos)
2. Criar `LESSONS_LEARNED.md` vazio com as seções e o formato de entrada definidos
3. Adicionar no `CLAUDE.md` (ou equivalente): "leia ARCHITECTURE.md antes de qualquer tarefa"

### Fase 2 — Primeiros sprints

4. Preencher seção de histórico de decisões no ARCHITECTURE.md a cada decisão tomada
5. Registrar toda lição no LESSONS_LEARNED.md enquanto o incidente ainda está fresco
6. Atualizar o estado das entregas no ARCHITECTURE.md ao fim de cada sprint

### Fase 3 — Operação contínua

7. ARCHITECTURE.md é lido no início de cada sessão de dev — a IA deve ser instruída a fazer isso
8. LESSONS_LEARNED.md é revisado antes de deploys e antes de features que tocam áreas de risco
9. Débitos abertos são revisados mensalmente — fechar ou reavaliar prioridade

### O que NÃO colocar nesses arquivos

| Não pertence aqui | Pertence em |
|---|---|
| Código ou snippets de implementação | O próprio código |
| Histórico de commits ou changelogs | git log |
| TODOs de curto prazo | TASKS_[feature].md |
| Documentação de API para usuários externos | README.md |
| Dados sensíveis ou credenciais | Jamais em arquivo de texto |

---

## Por que isso funciona em operação solo com IA

A IA não tem memória entre sessões. O ARCHITECTURE.md e o LESSONS_LEARNED.md
são a memória externalizada que transformam cada sessão nova num ponto de continuação,
não num recomeço.

A analogia correta: esses arquivos são para o Claude Code o que um briefing de contexto
é para um consultor sênior que entra num projeto na metade. Sem o briefing, o consultor
passa a primeira semana redescobindo o que a equipe já sabe. Com o briefing, opera
com produtividade plena desde o primeiro dia.

A diferença no Orbis.tax foi mensurável: sessões sem leitura prévia geravam colisões,
retrabalho e perguntas sobre estado do sistema. Sessões com leitura prévia dos dois arquivos
começavam direto na entrega.

---

*Gerado a partir da experiência operacional do Orbis.tax — Abril 2026*
