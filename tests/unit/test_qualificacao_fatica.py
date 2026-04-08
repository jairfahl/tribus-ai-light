"""
tests/unit/test_qualificacao_fatica.py — Testes unitários da Qualificação Fática (G23).

Verifica semáforo de completude, formatação de contexto e estrutura de campos.
Nenhuma chamada externa — stdlib apenas.
"""

import pytest

from src.cognitive.qualificacao_fatica import (
    CAMPOS_BASE,
    ResultadoQualificacao,
    calcular_semaforo,
    formatar_fatos_para_contexto,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FATOS_COMPLETOS = {
    "cnae_principal": "4711-3/02",
    "regime_tributario": "Lucro Real",
    "ufs_operacao": "SP, RJ",
    "tipo_operacao": "B2B",
    "faturamento_faixa": "R$ 50M a R$ 300M",
}

FATOS_PARCIAIS = {
    "cnae_principal": "4711-3/02",
    "regime_tributario": "Lucro Presumido",
    "ufs_operacao": "MG",
}

FATOS_INSUFICIENTES = {
    "cnae_principal": "1234",
}


# ---------------------------------------------------------------------------
# Semáforo
# ---------------------------------------------------------------------------

def test_semaforo_verde_com_todos_campos():
    r = calcular_semaforo(FATOS_COMPLETOS)
    assert r.semaforo == "verde"
    assert r.campos_faltando == []


def test_semaforo_amarelo_com_parcial():
    r = calcular_semaforo(FATOS_PARCIAIS)
    assert r.semaforo == "amarelo"
    assert len(r.campos_faltando) > 0


def test_semaforo_vermelho_com_insuficiente():
    r = calcular_semaforo(FATOS_INSUFICIENTES)
    assert r.semaforo == "vermelho"


def test_semaforo_vermelho_sem_fatos():
    r = calcular_semaforo({})
    assert r.semaforo == "vermelho"
    assert r.campos_preenchidos == 0


def test_semaforo_amarelo_limite_inferior():
    """Exatamente 3 campos preenchidos → amarelo."""
    fatos = {
        "cnae_principal": "1234",
        "regime_tributario": "Lucro Real",
        "ufs_operacao": "SP",
    }
    r = calcular_semaforo(fatos)
    assert r.semaforo == "amarelo"
    assert r.campos_preenchidos == 3


def test_semaforo_vermelho_dois_campos():
    """2 campos → vermelho."""
    fatos = {
        "cnae_principal": "1234",
        "regime_tributario": "Lucro Real",
    }
    r = calcular_semaforo(fatos)
    assert r.semaforo == "vermelho"


def test_cinco_campos_base_obrigatorios():
    obrigatorios = [k for k, v in CAMPOS_BASE.items() if v["obrigatorio"]]
    assert len(obrigatorios) == 5


# ---------------------------------------------------------------------------
# formatar_fatos_para_contexto
# ---------------------------------------------------------------------------

def test_formatar_fatos_com_dados():
    ctx = formatar_fatos_para_contexto(FATOS_COMPLETOS)
    assert "QUALIFICAÇÃO FÁTICA" in ctx
    assert "Lucro Real" in ctx
    assert "B2B" in ctx


def test_formatar_fatos_sem_dados():
    ctx = formatar_fatos_para_contexto({})
    assert "genérica" in ctx.lower()


def test_formatar_fatos_vermelho_aviso():
    """Fatos insuficientes devem gerar aviso de scoring rebaixado."""
    ctx = formatar_fatos_para_contexto(FATOS_INSUFICIENTES)
    assert "scoring_confianca" in ctx or "genérica" in ctx.lower()


def test_formatar_fatos_verde_sem_aviso():
    """Fatos completos não devem gerar aviso de análise genérica."""
    ctx = formatar_fatos_para_contexto(FATOS_COMPLETOS)
    assert "genérica" not in ctx.lower()


# ---------------------------------------------------------------------------
# ResultadoQualificacao
# ---------------------------------------------------------------------------

def test_resultado_campos_preenchidos_e_obrigatorios():
    r = calcular_semaforo(FATOS_COMPLETOS)
    assert r.campos_preenchidos == 5
    assert r.campos_obrigatorios == 5


def test_resultado_mensagem_nao_vazia():
    for fatos in [FATOS_COMPLETOS, FATOS_PARCIAIS, FATOS_INSUFICIENTES, {}]:
        r = calcular_semaforo(fatos)
        assert r.mensagem != "", f"Mensagem vazia para semáforo={r.semaforo}"
