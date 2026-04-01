"""
tests/unit/test_ptf.py — Testes do Pre-filter Temporal (PTF).

Testa extração de data_referencia, resolução de regime e flag de cenário futuro.
"""

import pytest
from datetime import date
from unittest.mock import patch

from src.rag.ptf import extrair_data_referencia, resolver_regime, is_future_scenario


class TestExtracaoDataReferencia:

    def test_ano_explicito_transicao(self):
        data = extrair_data_referencia("alíquota CBS em 2028")
        assert data == date(2028, 1, 1)

    def test_ano_explicito_definitivo(self):
        data = extrair_data_referencia("regime definitivo a partir de 2033")
        assert data == date(2033, 1, 1)

    def test_sem_data_retorna_none(self):
        data = extrair_data_referencia("qual a alíquota do IBS?")
        assert data is None

    def test_ano_vigente(self):
        data = extrair_data_referencia("PIS/COFINS em 2024")
        assert data == date(2024, 1, 1)

    def test_ano_com_contexto_exercicio(self):
        data = extrair_data_referencia("exercício fiscal de 2029")
        assert data == date(2029, 1, 1)

    def test_ano_com_contexto_periodo(self):
        data = extrair_data_referencia("no período de 2028 a 2030")
        assert data == date(2028, 1, 1)  # primeiro ano encontrado

    def test_ano_fora_do_range_inferior(self):
        data = extrair_data_referencia("legislação de 2020")
        assert data is None

    def test_query_vazia(self):
        data = extrair_data_referencia("")
        assert data is None

    def test_query_none(self):
        data = extrair_data_referencia(None)
        assert data is None

    def test_ano_2040(self):
        data = extrair_data_referencia("projeção para 2040")
        assert data == date(2040, 1, 1)

    def test_ano_2049_limite(self):
        data = extrair_data_referencia("cenário 2049")
        assert data == date(2049, 1, 1)

    def test_numero_nao_ano(self):
        """Números que não são anos não devem ser extraídos."""
        data = extrair_data_referencia("artigo 132 da constituição")
        assert data is None

    def test_primeiro_ano_da_query(self):
        """Se houver múltiplos anos, retorna o primeiro."""
        data = extrair_data_referencia("transição de 2027 até 2032")
        assert data == date(2027, 1, 1)


class TestResolverRegime:

    def test_regime_vigente_inicio(self):
        assert resolver_regime(date(2024, 1, 1)) == "vigente"

    def test_regime_vigente_fim(self):
        assert resolver_regime(date(2026, 12, 31)) == "vigente"

    def test_regime_transicao_inicio(self):
        assert resolver_regime(date(2027, 1, 1)) == "transicao"

    def test_regime_transicao_meio(self):
        assert resolver_regime(date(2029, 6, 15)) == "transicao"

    def test_regime_transicao_fim(self):
        assert resolver_regime(date(2032, 12, 31)) == "transicao"

    def test_regime_definitivo_inicio(self):
        assert resolver_regime(date(2033, 1, 1)) == "definitivo"

    def test_regime_definitivo_futuro(self):
        assert resolver_regime(date(2050, 1, 1)) == "definitivo"


class TestIsFutureScenario:

    def test_data_futura(self):
        assert is_future_scenario(date(2099, 1, 1)) is True

    def test_data_passada(self):
        assert is_future_scenario(date(2020, 1, 1)) is False

    def test_none(self):
        assert is_future_scenario(None) is False

    def test_data_hoje(self):
        """Data de hoje não é cenário futuro."""
        assert is_future_scenario(date.today()) is False


class TestRetrieveComPTF:
    """Testa que retrieve() aceita e propaga data_referencia."""

    @patch("src.rag.retriever._embed_query")
    @patch("src.rag.retriever.get_conn")
    @patch("src.rag.retriever.put_conn")
    def test_retrieve_com_data_referencia_gera_sql_correto(
        self, mock_put, mock_get_conn, mock_embed
    ):
        """Verifica que data_referencia adiciona cláusula WHERE temporal."""
        import psycopg2
        from unittest.mock import MagicMock

        mock_embed.return_value = [0.1] * 1024

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        from src.rag.retriever import retrieve

        resultado = retrieve("alíquota CBS em 2028", data_referencia=date(2028, 1, 1))

        # Verificar que a query SQL contém o filtro temporal
        call_args = mock_cursor.execute.call_args
        sql_executado = call_args[0][0]
        params_executados = call_args[0][1]

        assert "vigencia_inicio" in sql_executado
        assert "vigencia_fim" in sql_executado
        assert date(2028, 1, 1) in params_executados

    @patch("src.rag.retriever._embed_query")
    @patch("src.rag.retriever.get_conn")
    @patch("src.rag.retriever.put_conn")
    def test_retrieve_sem_data_referencia_nao_filtra(
        self, mock_put, mock_get_conn, mock_embed
    ):
        """Sem data_referencia, a query SQL não contém filtro temporal."""
        from unittest.mock import MagicMock

        mock_embed.return_value = [0.1] * 1024
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        from src.rag.retriever import retrieve

        retrieve("qual a alíquota do IBS?")

        call_args = mock_cursor.execute.call_args
        sql_executado = call_args[0][0]

        assert "vigencia_inicio" not in sql_executado
