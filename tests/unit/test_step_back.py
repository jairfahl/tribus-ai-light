"""
tests/unit/test_step_back.py — Testes do Step-Back Prompting (RDM-025).

Zero chamadas externas.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import date

from src.rag.step_back import (
    STEP_BACK_TIPOS_ELEGIVEIS,
    detectar_alta_especificidade,
    executar_step_back_fallback,
    gerar_step_back_query,
    retrieve_com_step_back,
)
from src.rag.retriever import ChunkResultado


def _chunk(chunk_id: int = 1, score_vetorial: float = 0.8,
           score_final: float = 0.75) -> ChunkResultado:
    return ChunkResultado(
        chunk_id=chunk_id,
        norma_codigo="LC214_2025",
        artigo="Art. 10",
        texto="Texto do chunk",
        score_vetorial=score_vetorial,
        score_bm25=0.5,
        score_final=score_final,
    )


# ── detectar_alta_especificidade ──────────────────────────────────


class TestDetectarAltaEspecificidade:

    def test_cnae_com_codigo_detectado(self):
        assert detectar_alta_especificidade(
            "Empresa com CNAE 4711-3/02 paga CBS?", "INTERPRETATIVA"
        ) is True

    def test_cnae_generico_detectado(self):
        assert detectar_alta_especificidade(
            "Qual CNAE 4711 tem redução?", "INTERPRETATIVA"
        ) is True

    def test_ncm_curto_detectado(self):
        assert detectar_alta_especificidade(
            "NCM 8471 importado tem crédito?", "COMPARATIVA"
        ) is True

    def test_ncm_longo_detectado(self):
        assert detectar_alta_especificidade(
            "Produto NCM com código 84713019 importado da China", "INTERPRETATIVA"
        ) is True

    def test_lucro_real_detectado(self):
        assert detectar_alta_especificidade(
            "Empresa no lucro real deve recolher CBS?", "INTERPRETATIVA"
        ) is True

    def test_lucro_presumido_detectado(self):
        assert detectar_alta_especificidade(
            "Contribuinte no lucro presumido tem crédito?", "COMPARATIVA"
        ) is True

    def test_simples_nacional_anexo_detectado(self):
        assert detectar_alta_especificidade(
            "Simples Nacional Anexo III tem alíquota diferenciada?", "INTERPRETATIVA"
        ) is True

    def test_operacao_interestadual_detectado(self):
        assert detectar_alta_especificidade(
            "Como funciona a operação interestadual no IBS?", "COMPARATIVA"
        ) is True

    def test_importacao_especifica_detectado(self):
        assert detectar_alta_especificidade(
            "importação de produto específico tem crédito?", "INTERPRETATIVA"
        ) is True

    def test_pessoa_fisica_ibs_detectado(self):
        assert detectar_alta_especificidade(
            "pessoa física que vende com IBS paga?", "INTERPRETATIVA"
        ) is True

    def test_microempresa_aliquota_detectado(self):
        assert detectar_alta_especificidade(
            "microempresa com alíquota reduzida no IBS?", "COMPARATIVA"
        ) is True

    def test_tipo_factual_nao_ativa(self):
        assert detectar_alta_especificidade(
            "Empresa com CNAE 4711 paga CBS?", "FACTUAL"
        ) is False

    def test_tipo_invalido_nao_ativa(self):
        assert detectar_alta_especificidade(
            "CNAE 4711 no lucro real", "OUTRO"
        ) is False

    def test_query_generica_nao_detectada(self):
        assert detectar_alta_especificidade(
            "Qual a alíquota de IBS em 2028?", "INTERPRETATIVA"
        ) is False

    def test_query_sem_indicadores_nao_detectada(self):
        assert detectar_alta_especificidade(
            "Como funciona o split payment?", "COMPARATIVA"
        ) is False

    def test_tipos_elegiveis_corretos(self):
        assert STEP_BACK_TIPOS_ELEGIVEIS == {"INTERPRETATIVA", "COMPARATIVA"}


# ── gerar_step_back_query ─────────────────────────────────────────


class TestGerarStepBackQuery:

    @patch("src.rag.step_back.anthropic.Anthropic")
    def test_gera_query_abstrata(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(
            text="Como incide CBS sobre transferências entre estabelecimentos?"
        )]
        mock_resp.usage.input_tokens = 80
        mock_resp.usage.output_tokens = 20
        mock_client.messages.create.return_value = mock_resp

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            result = gerar_step_back_query(
                "Empresa CNAE 4711-3/02 no lucro real deve pagar CBS?",
                "claude-haiku-4-5-20251001",
            )

        assert "transferências" in result or len(result) > 0
        mock_client.messages.create.assert_called_once()

    @patch("src.rag.step_back.anthropic.Anthropic")
    def test_temperatura_baixa(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(text="query abstrata")]
        mock_resp.usage.input_tokens = 50
        mock_resp.usage.output_tokens = 10
        mock_client.messages.create.return_value = mock_resp

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            gerar_step_back_query("test", "claude-haiku-4-5-20251001")

        call_kwargs = mock_client.messages.create.call_args[1]
        assert call_kwargs["temperature"] == 0.1

    @patch("src.rag.step_back.anthropic.Anthropic")
    def test_max_tokens_100(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(text="query abstrata")]
        mock_resp.usage.input_tokens = 50
        mock_resp.usage.output_tokens = 10
        mock_client.messages.create.return_value = mock_resp

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            gerar_step_back_query("test", "claude-haiku-4-5-20251001")

        call_kwargs = mock_client.messages.create.call_args[1]
        assert call_kwargs["max_tokens"] == 100

    @patch("src.rag.step_back.anthropic.Anthropic")
    def test_contexto_temporal_injetado(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(text="query abstrata")]
        mock_resp.usage.input_tokens = 50
        mock_resp.usage.output_tokens = 10
        mock_client.messages.create.return_value = mock_resp

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            gerar_step_back_query(
                "test", "claude-haiku-4-5-20251001",
                data_referencia=date(2028, 1, 1), regime="transicao",
            )

        call_kwargs = mock_client.messages.create.call_args[1]
        assert "2028" in call_kwargs["system"]
        assert "transicao" in call_kwargs["system"]

    def test_sem_api_key_levanta_erro(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(EnvironmentError):
                gerar_step_back_query("test", "claude-haiku-4-5-20251001")


# ── retrieve_com_step_back ────────────────────────────────────────


class TestRetrieveComStepBack:

    @patch("src.rag.step_back.retrieve")
    def test_fusao_deduplica_por_chunk_id(self, mock_retrieve):
        mock_retrieve.side_effect = [
            [_chunk(chunk_id=1, score_final=0.7)],
            [_chunk(chunk_id=1, score_final=0.9)],
        ]

        chunks, n_sb, n_esp = retrieve_com_step_back(
            "query original", "query abstrata", top_k=5,
        )

        assert len(chunks) == 1
        assert chunks[0].score_final == 0.9

    @patch("src.rag.step_back.retrieve")
    def test_fusao_chunks_diferentes(self, mock_retrieve):
        mock_retrieve.side_effect = [
            [_chunk(chunk_id=1, score_final=0.8)],
            [_chunk(chunk_id=2, score_final=0.7)],
        ]

        chunks, n_sb, n_esp = retrieve_com_step_back(
            "query original", "query abstrata", top_k=5,
        )

        assert len(chunks) == 2
        assert chunks[0].score_final >= chunks[1].score_final

    @patch("src.rag.step_back.retrieve")
    def test_proporcao_60_40(self, mock_retrieve):
        mock_retrieve.return_value = [_chunk()]

        retrieve_com_step_back(
            "query original", "query abstrata", top_k=5,
        )

        # step-back call: top_k=3 (60% of 5), original call: top_k=2 (40% of 5)
        calls = mock_retrieve.call_args_list
        assert len(calls) == 2
        assert calls[0][1]["top_k"] == 3  # step-back
        assert calls[1][1]["top_k"] == 2  # original

    @patch("src.rag.step_back.retrieve")
    def test_retorno_contagens(self, mock_retrieve):
        mock_retrieve.side_effect = [
            [_chunk(chunk_id=1), _chunk(chunk_id=2)],
            [_chunk(chunk_id=3)],
        ]

        chunks, n_sb, n_esp = retrieve_com_step_back(
            "query original", "query abstrata", top_k=5,
        )

        assert n_sb == 2
        assert n_esp == 1

    @patch("src.rag.step_back.retrieve")
    def test_limita_top_k(self, mock_retrieve):
        mock_retrieve.side_effect = [
            [_chunk(chunk_id=i, score_final=0.9 - i * 0.1) for i in range(3)],
            [_chunk(chunk_id=i + 10, score_final=0.8 - i * 0.1) for i in range(2)],
        ]

        chunks, _, _ = retrieve_com_step_back(
            "query original", "query abstrata", top_k=3,
        )

        assert len(chunks) <= 3

    @patch("src.rag.step_back.retrieve")
    def test_data_referencia_propagada(self, mock_retrieve):
        mock_retrieve.return_value = [_chunk()]
        data_ref = date(2028, 1, 1)

        retrieve_com_step_back(
            "query original", "query abstrata",
            data_referencia=data_ref,
        )

        for call in mock_retrieve.call_args_list:
            assert call[1]["data_referencia"] == data_ref


# ── executar_step_back_fallback ───────────────────────────────────


class TestExecutarStepBackFallback:

    def test_query_generica_nao_ativa(self):
        chunks_iniciais = [_chunk()]
        chunks, ativado, sb_query = executar_step_back_fallback(
            query="Qual a alíquota de IBS?",
            chunks_iniciais=chunks_iniciais,
            tipo_query="INTERPRETATIVA",
            model="claude-haiku-4-5-20251001",
        )
        assert ativado is False
        assert sb_query is None
        assert chunks == chunks_iniciais

    def test_tipo_factual_nao_ativa(self):
        chunks_iniciais = [_chunk()]
        chunks, ativado, sb_query = executar_step_back_fallback(
            query="Empresa CNAE 4711 paga CBS?",
            chunks_iniciais=chunks_iniciais,
            tipo_query="FACTUAL",
            model="claude-haiku-4-5-20251001",
        )
        assert ativado is False
        assert chunks == chunks_iniciais

    @patch("src.rag.step_back.retrieve_com_step_back")
    @patch("src.rag.step_back.gerar_step_back_query")
    def test_alta_especificidade_ativa(self, mock_gerar, mock_retrieve_sb):
        chunks_iniciais = [_chunk()]
        mock_gerar.return_value = "query abstrata sobre CBS"
        mock_retrieve_sb.return_value = ([_chunk(score_final=0.9)], 3, 2)

        chunks, ativado, sb_query = executar_step_back_fallback(
            query="Empresa com CNAE 4711 no lucro real deve pagar CBS?",
            chunks_iniciais=chunks_iniciais,
            tipo_query="INTERPRETATIVA",
            model="claude-haiku-4-5-20251001",
        )

        assert ativado is True
        assert sb_query == "query abstrata sobre CBS"

    @patch("src.rag.step_back.gerar_step_back_query", side_effect=Exception("LLM error"))
    def test_erro_retorna_chunks_iniciais(self, mock_gerar):
        chunks_iniciais = [_chunk()]
        chunks, ativado, sb_query = executar_step_back_fallback(
            query="Empresa com CNAE 4711 no lucro real paga CBS?",
            chunks_iniciais=chunks_iniciais,
            tipo_query="INTERPRETATIVA",
            model="claude-haiku-4-5-20251001",
        )

        assert ativado is False
        assert sb_query is None
        assert chunks == chunks_iniciais

    @patch("src.rag.step_back.retrieve_com_step_back")
    @patch("src.rag.step_back.gerar_step_back_query")
    def test_sem_resultados_mantem_iniciais(self, mock_gerar, mock_retrieve_sb):
        chunks_iniciais = [_chunk()]
        mock_gerar.return_value = "query abstrata"
        mock_retrieve_sb.return_value = ([], 0, 0)

        chunks, ativado, sb_query = executar_step_back_fallback(
            query="Empresa com CNAE 4711 no lucro real paga CBS?",
            chunks_iniciais=chunks_iniciais,
            tipo_query="INTERPRETATIVA",
            model="claude-haiku-4-5-20251001",
        )

        assert ativado is False
        assert sb_query == "query abstrata"
        assert chunks == chunks_iniciais

    @patch("src.rag.step_back.retrieve_com_step_back")
    @patch("src.rag.step_back.gerar_step_back_query")
    def test_propaga_parametros_retrieve(self, mock_gerar, mock_retrieve_sb):
        mock_gerar.return_value = "query abstrata"
        mock_retrieve_sb.return_value = ([_chunk()], 3, 2)
        data_ref = date(2028, 6, 1)

        executar_step_back_fallback(
            query="NCM 8471 importado tem crédito de IBS?",
            chunks_iniciais=[_chunk()],
            tipo_query="INTERPRETATIVA",
            model="claude-haiku-4-5-20251001",
            top_k=7,
            rerank_top_n=20,
            data_referencia=data_ref,
            regime="transicao",
        )

        call_kwargs = mock_retrieve_sb.call_args[1]
        assert call_kwargs["top_k"] == 7
        assert call_kwargs["rerank_top_n"] == 20
        assert call_kwargs["data_referencia"] == data_ref
