# Deploy VPS — Referência de Produção

## Informações Gerais

| Item | Valor |
|------|-------|
| Provider | Hostinger |
| IP | `69.62.100.24` |
| Domínio | https://orbis.tax |
| SSL | Let's Encrypt (expira 2026-07-11, renovação automática) |
| Arquivos prod | `/root/tribus-ai-light/` |
| Secrets | `/root/tribus-ai-light/.env.prod` (nunca commitar) |

---

## Stack de Produção

- `docker-compose.prod.yml` + nginx reverse proxy (portas 80 + 443)
- 4 serviços: `db`, `api`, `ui`, `nginx`
- Admin padrão: `admin@orbis.tax` / `Admin2026`

---

## Comandos Essenciais

```bash
# SSH para a VPS (alias configurado em ~/.ssh/config)
ssh orbis

# Redeploy completo
cd /root/tribus-ai-light && bash redeploy.sh

# Recriar serviço (relê .env.prod — USAR SEMPRE, não restart)
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d --force-recreate api

# Logs em tempo real
docker compose --env-file .env.prod -f docker-compose.prod.yml logs -f

# Fix de senha via container
docker exec -i tribus-ai-api python3 < /tmp/fix_hash.py

# Verificar variável de ambiente dentro do container
docker exec tribus-ai-api env | grep ASAAS
```

---

## Armadilhas Conhecidas

| Armadilha | Causa | Solução |
|-----------|-------|---------|
| `docker compose restart` não aplica nova env var | `restart` não relê `.env.prod` | Usar `up -d --force-recreate <serviço>` |
| `ASAAS_API_KEY` com `$` no .env.prod | Docker compose interpreta `$` como variável de shell | Usar `$$` no lugar de `$` |
| `ASAAS_BASE_URL` sandbox com chave de produção | Chave `$aact_prod_...` não autentica em `sandbox.asaas.com` → 401 → 500 para o usuário | `ASAAS_BASE_URL=https://api.asaas.com/v3` |
| `LOCKFILE_MODE=ENFORCE` | Valor inválido — causa startup error | Usar `WARN` ou `BLOCK` |
| Arquivos não commitados não chegam ao VPS | `redeploy.sh` faz `git pull` | `git status` + commit antes de push |

---

## Pré-Deploy Obrigatório

```bash
bash scripts/pre_deploy_check.sh
```

Zero erros = pode prosseguir. Qualquer erro = corrigir antes.

O script verifica: git status, testes backend, build frontend, LOCKFILE_MODE válido, secrets hardcoded, linters.

---

## Variáveis Obrigatórias no .env.prod

| Variável | Observação |
|----------|-----------|
| `DATABASE_URL` | Apontar para container `db` na rede Docker |
| `JWT_SECRET` | Sem fallback — RuntimeError se ausente |
| `ANTHROPIC_API_KEY` | Claude API |
| `VOYAGE_API_KEY` | Embeddings voyage-3 |
| `RESEND_API_KEY` | Obrigatória para e-mail de verificação |
| `ASAAS_API_KEY` | Iniciar com `$$` (escape docker compose) |
| `ASAAS_BASE_URL` | **Produção:** `https://api.asaas.com/v3` — NÃO usar sandbox com chave de produção |
| `LOCKFILE_MODE` | `WARN` (não `ENFORCE`) |
| `ZAPI_INSTANCE_ID` | ID da instância no painel Z-API |
| `ZAPI_TOKEN` | Token da instância no painel Z-API |
| `ZAPI_SECURITY_TOKEN` | Token de segurança (opcional, recomendado) |

---

## SSH — Configuração Local

Chave: `~/.ssh/orbis_vps`
Alias configurado em `~/.ssh/config`:

```
Host orbis
  HostName 69.62.100.24
  User root
  IdentityFile ~/.ssh/orbis_vps
```

Uso: `ssh orbis` (sem digitar IP ou credenciais)

---

## Domínios Registrados

- orbis.tax (principal)
- tribus-ai.com.br
- tribus-ia.com.br
