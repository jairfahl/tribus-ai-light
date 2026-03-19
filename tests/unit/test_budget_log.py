"""
Testes unitários para Context Budget Log.
Zero chamadas externas.
"""

from src.observability.budget_log import BudgetEntry, ContextBudgetLog, contar_tokens


class TestContextBudgetLog:

    def test_total_usado_soma_todas_entradas(self):
        log = ContextBudgetLog(prompt_codigo="v1.0", query_tipo="FACTUAL")
        log.adicionar("system_prompt_summary", "v1.0 [SUMMARY]", 500)
        log.adicionar("rag_chunks", "top-5 chunks", 3000)
        log.adicionar("instrucoes_saida", "json format", 200)
        assert log.total_usado == 3700

    def test_budget_disponivel_correto(self):
        log = ContextBudgetLog(prompt_codigo="v1.0", query_tipo="FACTUAL", budget_total=12100)
        log.adicionar("system_prompt_summary", "v1.0 [SUMMARY]", 600)
        log.adicionar("rag_chunks", "top-3 chunks", 2000)
        assert log.budget_disponivel == 12100 - 2600

    def test_alerta_pressao_acima_85(self):
        log = ContextBudgetLog(prompt_codigo="v1.0", query_tipo="COMPARATIVA", budget_total=12100)
        log.adicionar("system_prompt_summary", "summary", 600)
        log.adicionar("system_prompt_full", "full", 1200)
        log.adicionar("system_prompt_antialucinacao", "anti", 400)
        log.adicionar("rag_chunks", "chunks", 8100)  # total = 10300 > 85% of 12100
        assert log.alerta_pressao() is True
        assert log.pressao_pct > 85.0

    def test_sem_alerta_abaixo_85(self):
        log = ContextBudgetLog(prompt_codigo="v1.0", query_tipo="FACTUAL", budget_total=12100)
        log.adicionar("system_prompt_summary", "summary", 600)
        log.adicionar("rag_chunks", "chunks", 2000)
        assert log.alerta_pressao() is False

    def test_to_log_string_contem_todos_componentes(self):
        log = ContextBudgetLog(prompt_codigo="v1.0-test", query_tipo="INTERPRETATIVA")
        log.adicionar("system_prompt_summary", "v1.0 [SUMMARY]", 500)
        log.adicionar("system_prompt_full", "v1.0 [FULL]", 1000)
        log.adicionar("rag_chunks", "top-5 chunks", 3000)

        output = log.to_log_string()
        assert "[PROMPT:COMPOSE:START] v1.0-test query_tipo=INTERPRETATIVA" in output
        assert "[SYSTEM_PROMPT_SUMMARY] v1.0 [SUMMARY] 500 tokens" in output
        assert "[SYSTEM_PROMPT_FULL] v1.0 [FULL] 1000 tokens" in output
        assert "[RAG_CHUNKS] top-5 chunks 3000 tokens" in output
        assert "[PROMPT:COMPOSE:COMPLETE]" in output
        assert "Total: 4500 tokens" in output
        assert "Pressao:" in output

    def test_contar_tokens_retorna_inteiro_positivo(self):
        tokens = contar_tokens("Esta é uma frase de teste com algumas palavras.")
        assert isinstance(tokens, int)
        assert tokens > 0

    def test_budget_vazio_sem_entradas(self):
        log = ContextBudgetLog(prompt_codigo="v1.0", query_tipo="FACTUAL")
        assert log.total_usado == 0
        assert log.budget_disponivel == 12100
        assert log.alerta_pressao() is False
