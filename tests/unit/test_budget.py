"""
tests/unit/test_budget.py — Testes do Context Budget Manager (RDM-028).

Testa compactar_chunk, montar_contexto_budget e BUDGET_CONFIG.
Zero chamadas externas.
"""

import pytest

from src.cognitive.engine import (
    BUDGET_CONFIG,
    BUDGET_PRESSAO_THRESHOLD,
    ContextoBudgetResult,
    compactar_chunk,
    montar_contexto_budget,
)
from src.rag.retriever import ChunkResultado


def _chunk(texto: str = "", norma: str = "LC214_2025", artigo: str = "Art. 12",
           score: float = 0.87) -> ChunkResultado:
    """Helper para criar chunk de teste."""
    return ChunkResultado(
        chunk_id=1,
        norma_codigo=norma,
        artigo=artigo,
        texto=texto or (
            "O IBS incidirá sobre operações com bens e serviços. "
            "A alíquota será fixada por lei complementar. "
            "O regime de transição vigorará de 2027 a 2032. "
            "Após 2032, aplica-se o regime definitivo."
        ),
        score_vetorial=score,
        score_bm25=0.5,
        score_final=score,
    )


CHUNK_EXEMPLO = _chunk()


class TestCompactarChunk:

    def test_modo_full_contem_conteudo_completo(self):
        resultado = compactar_chunk(CHUNK_EXEMPLO, "FULL")
        assert "regime de transição" in resultado
        assert "LC214_2025" in resultado

    def test_modo_full_contem_score(self):
        resultado = compactar_chunk(CHUNK_EXEMPLO, "FULL")
        assert "score=0.870" in resultado

    def test_modo_summary_limita_sentencas(self):
        resultado = compactar_chunk(CHUNK_EXEMPLO, "SUMMARY")
        # Deve conter as 2 primeiras sentenças
        assert "O IBS incidirá" in resultado
        assert "A alíquota será fixada" in resultado
        # Não deve conter a 3ª sentença
        assert "regime de transição" not in resultado

    def test_modo_summary_contem_referencia(self):
        resultado = compactar_chunk(CHUNK_EXEMPLO, "SUMMARY")
        assert "RESUMO" in resultado
        assert "Art. 12" in resultado
        assert "LC214_2025" in resultado

    def test_modo_summary_contem_score(self):
        resultado = compactar_chunk(CHUNK_EXEMPLO, "SUMMARY")
        assert "score=0.870" in resultado

    def test_chunk_sem_artigo(self):
        chunk = _chunk(artigo=None)
        resultado = compactar_chunk(chunk, "FULL")
        assert "artigo não identificado" in resultado

    def test_chunk_texto_curto_summary(self):
        """Chunk com apenas 1 sentença retorna essa sentença no SUMMARY."""
        chunk = _chunk(texto="Apenas uma sentença.")
        resultado = compactar_chunk(chunk, "SUMMARY")
        assert "Apenas uma sentença." in resultado

    def test_full_preserva_texto_inteiro(self):
        texto_longo = "Sentença 1. " * 50
        chunk = _chunk(texto=texto_longo.strip())
        resultado = compactar_chunk(chunk, "FULL")
        assert texto_longo.strip() in resultado


class TestMontarContexto:

    def test_factual_usa_summary(self):
        chunks = [CHUNK_EXEMPLO] * 3
        resultado = montar_contexto_budget(chunks, "FACTUAL")
        assert resultado.modo == "SUMMARY"

    def test_interpretativa_usa_full(self):
        chunks = [CHUNK_EXEMPLO] * 3
        resultado = montar_contexto_budget(chunks, "INTERPRETATIVA")
        assert resultado.modo == "FULL"

    def test_comparativa_usa_full(self):
        chunks = [CHUNK_EXEMPLO] * 3
        resultado = montar_contexto_budget(chunks, "COMPARATIVA")
        assert resultado.modo == "FULL"

    def test_limite_chunks_factual(self):
        # FACTUAL tem max_chunks=5 — gerar 10 chunks e verificar descarte
        chunks = [CHUNK_EXEMPLO] * 10
        resultado = montar_contexto_budget(chunks, "FACTUAL")
        assert resultado.chunks_utilizados <= BUDGET_CONFIG["FACTUAL"]["max_chunks"]
        assert resultado.chunks_descartados >= 5

    def test_limite_chunks_interpretativa(self):
        chunks = [CHUNK_EXEMPLO] * 15
        resultado = montar_contexto_budget(chunks, "INTERPRETATIVA")
        assert resultado.chunks_utilizados <= BUDGET_CONFIG["INTERPRETATIVA"]["max_chunks"]

    def test_limite_chunks_comparativa(self):
        chunks = [CHUNK_EXEMPLO] * 20
        resultado = montar_contexto_budget(chunks, "COMPARATIVA")
        assert resultado.chunks_utilizados <= BUDGET_CONFIG["COMPARATIVA"]["max_chunks"]

    def test_pressao_pct_calculada(self):
        chunks = [CHUNK_EXEMPLO] * 3
        resultado = montar_contexto_budget(chunks, "FACTUAL")
        assert 0.0 <= resultado.pressao_pct <= 100.0

    def test_budget_log_formato(self):
        chunks = [CHUNK_EXEMPLO] * 2
        resultado = montar_contexto_budget(chunks, "COMPARATIVA")
        log = resultado.budget_log
        assert "tipo=COMPARATIVA" in log
        assert "modo=FULL" in log
        assert "pressao=" in log
        assert "chunks=" in log
        assert "tokens" in log

    def test_budget_log_factual_formato(self):
        chunks = [CHUNK_EXEMPLO] * 2
        resultado = montar_contexto_budget(chunks, "FACTUAL")
        assert "tipo=FACTUAL" in resultado.budget_log
        assert "modo=SUMMARY" in resultado.budget_log

    def test_descarte_por_tokens(self):
        """Chunks grandes que excedem max_tokens são descartados."""
        texto_grande = "Texto muito longo. " * 2000  # ~40k chars / ~10k tokens
        chunk_grande = _chunk(texto=texto_grande)
        chunks = [chunk_grande] * 5
        # Usar INTERPRETATIVA (modo FULL) para que o texto não seja compactado
        resultado = montar_contexto_budget(chunks, "INTERPRETATIVA")
        # INTERPRETATIVA max_tokens=12000, cada chunk ~10k tokens FULL
        assert resultado.chunks_utilizados < 5
        assert resultado.chunks_descartados > 0

    def test_sem_chunks_retorna_vazio(self):
        resultado = montar_contexto_budget([], "FACTUAL")
        assert resultado.chunks_utilizados == 0
        assert resultado.chunks_descartados == 0
        assert resultado.contexto_texto == ""
        assert resultado.tokens_estimados == 0

    def test_tipo_desconhecido_usa_interpretativa(self):
        """Tipo de query desconhecido cai no fallback INTERPRETATIVA."""
        chunks = [CHUNK_EXEMPLO] * 3
        resultado = montar_contexto_budget(chunks, "DESCONHECIDO")
        assert resultado.modo == "FULL"

    def test_contexto_texto_separa_com_divisor(self):
        chunks = [CHUNK_EXEMPLO] * 2
        resultado = montar_contexto_budget(chunks, "INTERPRETATIVA")
        assert "\n\n---\n\n" in resultado.contexto_texto

    def test_resultado_tipo_correto(self):
        resultado = montar_contexto_budget([CHUNK_EXEMPLO], "FACTUAL")
        assert isinstance(resultado, ContextoBudgetResult)

    def test_tokens_estimados_positivo_com_chunks(self):
        resultado = montar_contexto_budget([CHUNK_EXEMPLO], "FACTUAL")
        assert resultado.tokens_estimados > 0

    def test_nao_excede_max_tokens(self):
        """Nenhum tipo de query excede max_tokens_contexto definido."""
        for tipo, config in BUDGET_CONFIG.items():
            chunks = [CHUNK_EXEMPLO] * 20
            resultado = montar_contexto_budget(chunks, tipo)
            assert resultado.tokens_estimados <= config["max_tokens_contexto"], (
                f"{tipo}: tokens_estimados={resultado.tokens_estimados} > max={config['max_tokens_contexto']}"
            )
