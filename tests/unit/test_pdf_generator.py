"""
Testes unitários do módulo src/export/pdf_generator.py.
WeasyPrint é mockado — sem dependências de sistema no CI.
"""
import json
from unittest.mock import MagicMock, patch

import pytest

from src.export.pdf_generator import (
    CLASSE_CONFIG,
    _build_context_analysis,
    _build_context_dossie,
    _compute_integrity_hash,
    _render_html,
    generate_pdf,
    pdf_filename,
)


# ---------------------------------------------------------------------------
# _compute_integrity_hash
# ---------------------------------------------------------------------------

def test_integrity_hash_is_sha256():
    data = {"p1": "foo", "p2": "bar"}
    h = _compute_integrity_hash(data)
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


def test_integrity_hash_deterministic():
    data = {"x": "hello"}
    assert _compute_integrity_hash(data) == _compute_integrity_hash(data)


def test_integrity_hash_changes_with_content():
    assert _compute_integrity_hash({"a": "1"}) != _compute_integrity_hash({"a": "2"})


# ---------------------------------------------------------------------------
# _build_context_analysis
# ---------------------------------------------------------------------------

def test_build_context_analysis_basic():
    data = {
        "resposta": "Texto da análise.",
        "grau_consolidacao": "Alto",
        "saidas_stakeholders": [
            {"emoji": "📊", "label": "Financeiro", "stakeholder_id": "fin", "resumo": "Impacto X"}
        ],
    }
    ctx = _build_context_analysis(data, {"nome": "Empresa ABC", "cnpj": "00.000.000/0001-00"})
    assert ctx["source_type"] == "analysis"
    assert ctx["conteudo_principal"] == "Texto da análise."
    assert ctx["tenant_nome"] == "Empresa ABC"
    assert ctx["tenant_cnpj"] == "00.000.000/0001-00"
    assert ctx["is_dossie"] is False
    assert len(ctx["stakeholder_views"]) == 1
    assert ctx["stakeholder_views"][0]["resumo"] == "Impacto X"


def test_build_context_analysis_default_disclaimer():
    ctx = _build_context_analysis({})
    assert "Reforma Tributária" in ctx["disclaimer"]


def test_build_context_analysis_scoring_normalized():
    # scoring <= 1.0 deve ser convertido para percentual inteiro
    ctx = _build_context_analysis({"scoring_confianca": 0.87})
    assert ctx["gov_scoring"] == 87


# ---------------------------------------------------------------------------
# _build_context_dossie — watermarks e classes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("classe,expected_wm", [
    ("dossie_decisao", "DOSSIÊ"),
    ("recomendacao_formal", "RECOMENDAÇÃO"),
    ("alerta", "ALERTA"),
])
def test_watermark_por_classe(classe, expected_wm):
    ctx = _build_context_dossie({"classe": classe})
    assert ctx["watermark_text"] == expected_wm


def test_dossie_legalhold():
    ctx = _build_context_dossie({"classe": "dossie_decisao", "conteudo": {"p1": "foo"}})
    assert ctx["legalhold"] is True
    assert ctx["integrity_hash"] is not None


def test_nota_trabalho_no_legalhold():
    ctx = _build_context_dossie({"classe": "nota_trabalho", "conteudo": "texto livre"})
    assert ctx["legalhold"] is False
    assert ctx["integrity_hash"] is None


def test_dossie_extrai_passos_p1_p6():
    conteudo = {f"p{i}": f"Texto do passo {i}" for i in range(1, 7)}
    ctx = _build_context_dossie({"classe": "dossie_decisao", "conteudo": conteudo})
    assert ctx["is_dossie"] is True
    assert ctx["passos"] is not None
    assert len(ctx["passos"]) == 6
    assert ctx["passos"][0]["num"] == 1


# ---------------------------------------------------------------------------
# _render_html
# ---------------------------------------------------------------------------

def test_render_html_contains_titulo():
    ctx = _build_context_analysis({"resposta": "conteúdo", "titulo": "Meu Relatório"})
    html = _render_html(ctx)
    assert "Meu Relatório" in html


def test_render_html_contains_hash_for_dossie():
    conteudo = {"p1": "dado importante"}
    ctx = _build_context_dossie({"classe": "dossie_decisao", "conteudo": conteudo})
    html = _render_html(ctx)
    assert "SHA-256" in html
    assert ctx["integrity_hash"] in html


# ---------------------------------------------------------------------------
# generate_pdf — mock WeasyPrint
# ---------------------------------------------------------------------------

def test_generate_pdf_calls_weasyprint():
    fake_bytes = b"%PDF-1.4 fake"
    mock_html_instance = MagicMock()
    mock_html_instance.write_pdf.return_value = fake_bytes

    with patch("src.export.pdf_generator.HTML", return_value=mock_html_instance) as mock_html:
        result = generate_pdf("analysis", {"resposta": "teste"})

    assert result == fake_bytes
    mock_html.assert_called_once()


def test_generate_pdf_dossie_with_hash():
    fake_bytes = b"%PDF-1.4 fake"
    mock_html_instance = MagicMock()
    mock_html_instance.write_pdf.return_value = fake_bytes

    with patch("src.export.pdf_generator.HTML", return_value=mock_html_instance):
        result = generate_pdf(
            "dossie",
            {"classe": "dossie_decisao", "conteudo": {"p1": "foo"}, "titulo": "Meu Dossiê"},
        )
    assert result == fake_bytes


# ---------------------------------------------------------------------------
# pdf_filename
# ---------------------------------------------------------------------------

def test_pdf_filename_analysis():
    name = pdf_filename("analysis")
    assert name.startswith("orbis_orientacao_")
    assert name.endswith(".pdf")


def test_pdf_filename_dossie():
    name = pdf_filename("dossie", "dossie_decisao")
    assert name.startswith("orbis_dossie_")
    assert name.endswith(".pdf")


def test_pdf_filename_recomendacao():
    name = pdf_filename("dossie", "recomendacao_formal")
    assert "recomendacao" in name
