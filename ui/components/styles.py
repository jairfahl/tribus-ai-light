"""
ui/components/styles.py — Sistema de Design Global (Tribus-AI).

CSS injetado uma única vez no app via inject_global_css().
Paleta e tipografia alinhadas com a landing page.

O que este módulo controla (implementável no Streamlit):
  ✅ Tipografia: fonte Inter, hierarquia h1-h3, line-height
  ✅ Paleta: azul-escuro #1F3864, azul-medio #2E75B6, destaque #F59E0B
  ✅ Cards: containers com borda, fundo e padding
  ✅ Tabs: sublinhado ativo, cor do texto
  ✅ Métricas: label e valor padronizados
  ✅ Expanders: borda sutil, ícone colorido
  ✅ Badges HTML: .tm-badge-* (crítico, atenção, informativo, hold)
  ✅ Alertas: info/warning/error/success com borda esquerda
  ✅ Sidebar: fundo levemente azulado
  ✅ Botão primário: cor da marca
  ✅ Dividers: cor mais sutil

O que NÃO está aqui (não implementável no Streamlit):
  ❌ position absolute / z-index fora do tooltip
  ❌ animações interativas
  ❌ hover states em st.button
  ❌ modais/overlays
  ❌ responsividade mobile real
"""

from __future__ import annotations

import streamlit as st

_CSS_INJECTED = False

# ── Paleta — alinhada com landing/index.html ─────────────────────────────────
_AZUL_ESCURO  = "#1F3864"
_AZUL_MEDIO   = "#2E75B6"
_AZUL_CLARO   = "#E8F0FA"
_CINZA_TEXTO  = "#4A5568"
_CINZA_CLARO  = "#F5F7FA"
_BORDA        = "#E2E8F0"
_DESTAQUE     = "#F59E0B"
_BRANCO       = "#FFFFFF"

_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ───────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    color: {_CINZA_TEXTO};
    -webkit-font-smoothing: antialiased;
}}

/* ── Tipografia ─────────────────────────────────────────────────────────── */
h1 {{
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: {_AZUL_ESCURO} !important;
    line-height: 1.2 !important;
    margin-bottom: 8px !important;
}}
h2 {{
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: {_AZUL_ESCURO} !important;
    line-height: 1.3 !important;
}}
h3, h4 {{
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: {_AZUL_ESCURO} !important;
}}
p, .stMarkdown p {{
    line-height: 1.65 !important;
    color: {_CINZA_TEXTO};
}}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background-color: {_CINZA_CLARO} !important;
    border-right: 1px solid {_BORDA} !important;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {_AZUL_ESCURO} !important;
}}

/* ── Tabs ───────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    border-bottom: 2px solid {_BORDA} !important;
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: {_CINZA_TEXTO} !important;
    padding: 10px 16px !important;
    border-radius: 6px 6px 0 0 !important;
}}
.stTabs [aria-selected="true"] {{
    color: {_AZUL_MEDIO} !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {_AZUL_MEDIO} !important;
    background: {_AZUL_CLARO} !important;
}}

/* ── Expanders ──────────────────────────────────────────────────────────── */
.stExpander {{
    border: 1px solid {_BORDA} !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    margin-bottom: 8px !important;
}}
.stExpander summary {{
    font-weight: 600 !important;
    color: {_AZUL_ESCURO} !important;
    background: {_CINZA_CLARO} !important;
    padding: 10px 16px !important;
}}
.stExpander summary:hover {{
    background: {_AZUL_CLARO} !important;
}}

/* ── Métricas ───────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: {_BRANCO};
    border: 1px solid {_BORDA};
    border-radius: 8px;
    padding: 16px 20px !important;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {_CINZA_TEXTO} !important;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: {_AZUL_ESCURO} !important;
}}

/* ── Botão primário ─────────────────────────────────────────────────────── */
.stButton button[kind="primary"],
.stButton button[data-testid="baseButton-primary"] {{
    background-color: {_AZUL_MEDIO} !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 20px !important;
    color: {_BRANCO} !important;
}}
.stButton button[kind="secondary"],
.stButton button[data-testid="baseButton-secondary"] {{
    border: 1.5px solid {_AZUL_MEDIO} !important;
    border-radius: 8px !important;
    color: {_AZUL_MEDIO} !important;
    font-weight: 500 !important;
}}

/* ── Inputs e selects ───────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] {{
    border-radius: 6px !important;
    border-color: {_BORDA} !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: {_AZUL_MEDIO} !important;
    box-shadow: 0 0 0 2px {_AZUL_CLARO} !important;
}}

/* ── Alertas: borda esquerda colorida ───────────────────────────────────── */
[data-testid="stAlert"] {{
    border-radius: 8px !important;
    border-left-width: 4px !important;
    border-left-style: solid !important;
}}
[data-testid="stAlert"][data-type="info"] {{
    border-left-color: {_AZUL_MEDIO} !important;
    background: {_AZUL_CLARO} !important;
}}
[data-testid="stAlert"][data-type="warning"] {{
    border-left-color: {_DESTAQUE} !important;
    background: #fffbeb !important;
}}
[data-testid="stAlert"][data-type="error"] {{
    border-left-color: #e53e3e !important;
}}
[data-testid="stAlert"][data-type="success"] {{
    border-left-color: #38a169 !important;
}}

/* ── Dividers ───────────────────────────────────────────────────────────── */
hr {{
    border-color: {_BORDA} !important;
    margin: 16px 0 !important;
}}

/* ── Dataframe header ───────────────────────────────────────────────────── */
[data-testid="stDataFrame"] th {{
    background-color: {_CINZA_CLARO} !important;
    color: {_AZUL_ESCURO} !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

/* ── Caption ────────────────────────────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] {{
    color: #718096 !important;
    font-size: 0.82rem !important;
    line-height: 1.55 !important;
}}

/* ── Card helper — usar via st.markdown('<div class="tm-card">...</div>') ─ */
.tm-card {{
    background: {_BRANCO};
    border: 1px solid {_BORDA};
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(31,56,100,.06);
}}
.tm-card-azul {{
    background: {_AZUL_CLARO};
    border: 1px solid #c3d8f0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 8px;
}}
.tm-card-destaque {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid {_DESTAQUE};
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
}}

/* ── Badges HTML customizados ───────────────────────────────────────────── */
.tm-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}
.tm-badge-critico   {{ background: #fee2e2; color: #991b1b; }}
.tm-badge-atencao   {{ background: #fef3c7; color: #92400e; }}
.tm-badge-info      {{ background: {_AZUL_CLARO}; color: {_AZUL_ESCURO}; }}
.tm-badge-hold      {{ background: #f3e8ff; color: #6b21a8; }}
.tm-badge-memoria   {{ background: #ecfdf5; color: #065f46; }}

/* ── Label de seção (igual landing page) ────────────────────────────────── */
.tm-label {{
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {_AZUL_MEDIO};
    background: {_AZUL_CLARO};
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
}}

/* ── Scrollbar ──────────────────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {_CINZA_CLARO}; }}
::-webkit-scrollbar-thumb {{ background: #c1cdd6; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {_AZUL_MEDIO}; }}
"""


def inject_global_css() -> None:
    """
    Injeta o CSS do sistema de design uma única vez por sessão.
    Chamar no início de app.py, após _verificar_autenticacao().
    """
    global _CSS_INJECTED  # noqa: PLW0603
    if _CSS_INJECTED:
        return
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
    _CSS_INJECTED = True
