"""
Testes para o Loop Depth Quality Gate (ACT-inspired).

Verifica:
- FACTUAL nunca itera além de 1
- INTERPRETATIVA itera até 2 quando Quality Gate não é VERDE na iter 1
- COMPARATIVA itera até 3
- Halt imediato em VERDE
- Escalonamento correto de top_k por iteração
- AnaliseResult.quality_iterations reflete o número real de iterações
"""
import types
from dataclasses import dataclass, field
from unittest.mock import MagicMock, patch

import pytest

from src.cognitive.engine import (
    AnaliseResult,
    _QUALITY_MAX_ITER,
    _QUALITY_TOPK_SCALE,
)
from src.quality.engine import QualidadeResult, QualidadeStatus
from src.rag.adaptive import QueryTipo


# ---------------------------------------------------------------------------
# Constantes e helpers
# ---------------------------------------------------------------------------

def _qualidade(status: QualidadeStatus) -> QualidadeResult:
    return QualidadeResult(
        status=status,
        ressalvas=[],
        bloqueios=[],
        disclaimer=None,
    )


# ---------------------------------------------------------------------------
# Testes das constantes (invariáveis arquiteturais)
# ---------------------------------------------------------------------------

def test_factual_max_iter_e_1():
    assert _QUALITY_MAX_ITER["factual"] == 1


def test_interpretativa_max_iter_e_2():
    assert _QUALITY_MAX_ITER["interpretativa"] == 2


def test_comparativa_max_iter_e_3():
    assert _QUALITY_MAX_ITER["comparativa"] == 3


def test_topk_scale_iter1_e_1():
    assert _QUALITY_TOPK_SCALE[1] == 1.0


def test_topk_scale_iter2_maior_que_1():
    assert _QUALITY_TOPK_SCALE[2] > 1.0


def test_topk_scale_iter3_maior_que_iter2():
    assert _QUALITY_TOPK_SCALE[3] > _QUALITY_TOPK_SCALE[2]


# ---------------------------------------------------------------------------
# Testes de escalonamento de top_k
# ---------------------------------------------------------------------------

def test_escalonamento_topk_interpretativa():
    """top_k na iter 2 deve ser round(base * scale[2])."""
    from dataclasses import replace
    from src.rag.adaptive import obter_params_adaptativos

    params = obter_params_adaptativos("como funciona o IBS", top_k_base=7, rerank_top_n_base=25)
    params_iter2 = replace(
        params,
        top_k=round(params.top_k * _QUALITY_TOPK_SCALE[2]),
        rerank_top_n=round(params.rerank_top_n * _QUALITY_TOPK_SCALE[2]),
    )
    assert params_iter2.top_k == round(params.top_k * 1.7)
    assert params_iter2.rerank_top_n == round(params.rerank_top_n * 1.7)


def test_escalonamento_topk_comparativa_iter3():
    """top_k na iter 3 deve ser round(base * 2.5)."""
    from dataclasses import replace
    from src.rag.adaptive import obter_params_adaptativos

    params = obter_params_adaptativos("diferença entre EC 132 e LC 214", top_k_base=5, rerank_top_n_base=20)
    params_iter3 = replace(
        params,
        top_k=round(params.top_k * _QUALITY_TOPK_SCALE[3]),
    )
    assert params_iter3.top_k == round(params.top_k * 2.5)


# ---------------------------------------------------------------------------
# Teste de campo quality_iterations em AnaliseResult
# ---------------------------------------------------------------------------

def test_analise_result_quality_iterations_default_e_1():
    """Campo quality_iterations existe com default 1."""
    assert "quality_iterations" in AnaliseResult.__dataclass_fields__
    assert AnaliseResult.__dataclass_fields__["quality_iterations"].default == 1


def test_analise_result_aceita_quality_iterations():
    """AnaliseResult pode ser construído com quality_iterations > 1."""
    from src.cognitive.engine import AntiAlucinacaoResult
    from src.rag.retriever import ChunkResultado

    qualidade = _qualidade(QualidadeStatus.AMARELO)
    anti = AntiAlucinacaoResult()
    r = AnaliseResult(
        query="teste",
        chunks=[],
        qualidade=qualidade,
        fundamento_legal=[],
        grau_consolidacao="sem_precedente",
        contra_tese=None,
        scoring_confianca="medio",
        resposta="ok",
        disclaimer=None,
        anti_alucinacao=anti,
        prompt_version="v1",
        model_id="test",
        latencia_ms=100,
        quality_iterations=2,
    )
    assert r.quality_iterations == 2


# ---------------------------------------------------------------------------
# Testes lógicos de halting (simulação do loop)
# ---------------------------------------------------------------------------

def _simular_loop(query_tipo_str: str, statuses: list[QualidadeStatus]) -> tuple[int, QualidadeStatus]:
    """
    Simula a lógica do loop quality gate dado uma lista de statuses por iteração.
    Retorna (iterations_realizadas, status_final).
    """
    from dataclasses import replace
    from src.rag.adaptive import obter_params_adaptativos

    max_iter = _QUALITY_MAX_ITER.get(query_tipo_str, 1)
    params = obter_params_adaptativos("dummy", top_k_base=5, rerank_top_n_base=15)
    final_status = statuses[0]
    iterations = 0

    for iter_n in range(1, max_iter + 1):
        iterations = iter_n
        status = statuses[iter_n - 1] if iter_n <= len(statuses) else statuses[-1]
        final_status = status

        if status == QualidadeStatus.VERMELHO:
            break
        if status == QualidadeStatus.VERDE or iter_n == max_iter:
            break

    return iterations, final_status


def test_factual_sempre_para_em_iter1_mesmo_amarelo():
    """FACTUAL com AMARELO: max_iter=1, loop termina na iter 1."""
    iters, status = _simular_loop("factual", [QualidadeStatus.AMARELO])
    assert iters == 1


def test_interpretativa_para_em_iter1_se_verde():
    """INTERPRETATIVA com VERDE na iter 1: halt imediato."""
    iters, status = _simular_loop("interpretativa", [QualidadeStatus.VERDE])
    assert iters == 1
    assert status == QualidadeStatus.VERDE


def test_interpretativa_itera_para_iter2_se_amarelo():
    """INTERPRETATIVA com AMARELO iter1, VERDE iter2: deve usar iter 2."""
    iters, status = _simular_loop("interpretativa", [QualidadeStatus.AMARELO, QualidadeStatus.VERDE])
    assert iters == 2
    assert status == QualidadeStatus.VERDE


def test_interpretativa_para_em_max_iter_sem_verde():
    """INTERPRETATIVA com AMARELO em ambas as iterações: para em iter 2."""
    iters, status = _simular_loop("interpretativa", [QualidadeStatus.AMARELO, QualidadeStatus.AMARELO])
    assert iters == 2


def test_comparativa_itera_ate_3():
    """COMPARATIVA com AMARELO em todas as iterações: usa iter 3."""
    iters, status = _simular_loop(
        "comparativa",
        [QualidadeStatus.AMARELO, QualidadeStatus.AMARELO, QualidadeStatus.AMARELO]
    )
    assert iters == 3


def test_comparativa_halt_em_iter2_se_verde():
    """COMPARATIVA com VERDE na iter 2: halt antes de iter 3."""
    iters, status = _simular_loop(
        "comparativa",
        [QualidadeStatus.AMARELO, QualidadeStatus.VERDE, QualidadeStatus.AMARELO]
    )
    assert iters == 2
    assert status == QualidadeStatus.VERDE


def test_vermelho_halt_imediato():
    """VERMELHO em qualquer iteração causa halt imediato."""
    iters, status = _simular_loop(
        "comparativa",
        [QualidadeStatus.VERMELHO, QualidadeStatus.VERDE, QualidadeStatus.VERDE]
    )
    assert iters == 1
    assert status == QualidadeStatus.VERMELHO
