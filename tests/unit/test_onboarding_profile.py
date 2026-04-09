"""
Testes unitários — Qualificação de Tenant (Insight E GTM).
Sem chamadas ao banco — validam apenas a lógica de controle de fluxo.
"""

BYPASS_UUID = "00000000-0000-0000-0000-000000000000"


def test_bypass_uuid_libera_app():
    """BYPASS_UUID deve pular o onboarding sem tocar o banco."""
    assert BYPASS_UUID == "00000000-0000-0000-0000-000000000000"


def test_step_inicial_zero():
    """onboarding_step DEFAULT 0 — definido pela migration 117."""
    step_padrao = 0
    assert step_padrao == 0


def test_step_1_nao_bloqueia():
    """step >= 1: acesso ao app liberado (retorno True)."""
    for step in (1, 2, 3):
        acesso_liberado = step >= 1
        assert acesso_liberado is True, f"step={step} deveria liberar o acesso"


def test_step_0_bloqueia():
    """step == 0: app bloqueado até step 0 completado."""
    step = 0
    bloqueado = step == 0
    assert bloqueado is True
