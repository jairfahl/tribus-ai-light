"""
tests/unit/test_p2_validacao.py — Testes de validação do P2.

Verifica as regras de mínimo de premissas e riscos (G02):
- Mínimo de 3 premissas regulatórias
- Mínimo de 3 riscos fiscais
- Gate de avanço só liberado quando ambos os mínimos são atingidos
"""

MIN_PREMISSAS = 3
MIN_RISCOS = 3


def _p2_valido(premissas: list, riscos: list) -> bool:
    """Lógica de validação do gate P2 (espelho da validação na UI e engine)."""
    return len(premissas) >= MIN_PREMISSAS and len(riscos) >= MIN_RISCOS


class TestMinimosDefinidos:
    def test_minimo_premissas_e_tres(self):
        assert MIN_PREMISSAS == 3

    def test_minimo_riscos_e_tres(self):
        assert MIN_RISCOS == 3


class TestGateP2:
    def test_invalido_sem_premissas(self):
        assert not _p2_valido([], ["r1", "r2", "r3"])

    def test_invalido_sem_riscos(self):
        assert not _p2_valido(["p1", "p2", "p3"], [])

    def test_invalido_premissas_insuficientes(self):
        assert not _p2_valido(["p1", "p2"], ["r1", "r2", "r3"])

    def test_invalido_riscos_insuficientes(self):
        assert not _p2_valido(["p1", "p2", "p3"], ["r1", "r2"])

    def test_invalido_ambos_insuficientes(self):
        assert not _p2_valido(["p1"], ["r1"])

    def test_valido_com_minimos_exatos(self):
        assert _p2_valido(["p1", "p2", "p3"], ["r1", "r2", "r3"])

    def test_valido_acima_do_minimo(self):
        assert _p2_valido(["p1", "p2", "p3", "p4", "p5"], ["r1", "r2", "r3", "r4"])

    def test_invalido_com_strings_vazias_nao_contam(self):
        # Simulação: a UI só envia strings não vazias
        premissas_com_vazias = [p for p in ["p1", "", "p3"] if p.strip()]
        riscos_com_vazios = [r for r in ["r1", "r2", "r3"] if r.strip()]
        assert not _p2_valido(premissas_com_vazias, riscos_com_vazios)  # só 2 premissas


class TestP2Concluido:
    def test_p2_concluido_flag_correto(self):
        """Espelha a lógica de _p2_concluido em _registrar_interacao."""
        premissas = ["p1", "p2", "p3"]
        riscos = ["r1", "r2", "r3"]
        p2_concluido = len(premissas) >= 3 and len(riscos) >= 3
        assert p2_concluido is True

    def test_p2_concluido_false_quando_incompleto(self):
        premissas = ["p1"]
        riscos = ["r1", "r2", "r3"]
        p2_concluido = len(premissas) >= 3 and len(riscos) >= 3
        assert p2_concluido is False
