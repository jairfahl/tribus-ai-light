"""
tests/unit/test_proatividade.py — Testes unitários da Proatividade Customizada (D5, G25).
"""

from src.cognitive.proatividade import (
    JANELA_DIAS,
    SILENCIO_PADRAO_DIAS,
    TEMAS_CONFIG,
    THRESHOLD_SUGESTAO,
    SugestaoProativa,
    detectar_padroes,
    gerar_sugestoes,
    registrar_tags_analise,
)


def test_threshold_definido():
    assert THRESHOLD_SUGESTAO == 3


def test_janela_noventa_dias():
    assert JANELA_DIAS == 90


def test_silencio_padrao_trinta_dias():
    assert SILENCIO_PADRAO_DIAS == 30


def test_temas_config_nao_vazio():
    assert len(TEMAS_CONFIG) >= 8


def test_todos_temas_tem_label():
    for tema, label in TEMAS_CONFIG.items():
        assert len(label) > 5, f"Label muito curto para tema '{tema}'"


def test_bypass_uuid_detectar_padroes_retorna_vazio():
    BYPASS = "00000000-0000-0000-0000-000000000000"
    resultado = detectar_padroes(BYPASS)
    assert resultado == []


def test_none_detectar_padroes_retorna_vazio():
    resultado = detectar_padroes(None)
    assert resultado == []


def test_bypass_uuid_registrar_tags_silencioso():
    BYPASS = "00000000-0000-0000-0000-000000000000"
    # Não deve lançar exceção
    registrar_tags_analise(BYPASS, ["cbs", "ibs"])


def test_none_registrar_tags_silencioso():
    registrar_tags_analise(None, ["cbs"])


def test_sugestao_proativa_dataclass():
    s = SugestaoProativa(
        tema="creditamento",
        tema_label="Creditamento IBS/CBS",
        contagem=5,
        mensagem="Identificamos 5 análises sobre Creditamento IBS/CBS nos últimos 90 dias.",
        acao_sugerida="Deseja monitorar?",
    )
    assert s.contagem == 5
    assert "Creditamento" in s.mensagem
    assert s.tema == "creditamento"


def test_bypass_gerar_sugestoes_retorna_vazio():
    BYPASS = "00000000-0000-0000-0000-000000000000"
    resultado = gerar_sugestoes(BYPASS)
    assert resultado == []
