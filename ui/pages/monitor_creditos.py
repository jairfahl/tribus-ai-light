"""
ui/pages/monitor_creditos.py — MP-02 Monitor de Créditos IBS/CBS.

Renderiza mapeamento de créditos por categoria de aquisição,
alertas de glosa e oportunidades de recuperação.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.simuladores.creditos_ibs_cbs import (
    CATEGORIAS_AQUISICAO,
    ItemAquisicao,
    TipoCreditamento,
    formatar_brl,
    mapear_creditos,
)

_TIPO_BADGE = {
    TipoCreditamento.INTEGRAL:   "Integral",
    TipoCreditamento.PRESUMIDO:  "Presumido",
    TipoCreditamento.PARCIAL:    "Parcial",
    TipoCreditamento.NENHUM:     "Nenhum",
    TipoCreditamento.INDEFINIDO: "Indefinido",
}

_RISCO_BADGE = {"baixo": "🟢", "medio": "🟡", "alto": "🔴"}


def render_monitor_creditos() -> None:
    st.header("Monitor de Créditos IBS/CBS — MP-02")
    st.caption(
        "Mapeia créditos gerados nas aquisições, identifica créditos em risco "
        "e oportunidades de recuperação. LC 214/2025, arts. 28–55."
    )

    st.subheader("Informe suas aquisições mensais por categoria")
    st.caption("Preencha apenas as categorias aplicáveis ao seu negócio.")

    itens = []
    for cat_id, config in CATEGORIAS_AQUISICAO.items():
        risco_badge = _RISCO_BADGE.get(config["risco"], "⚪")
        valor = st.number_input(
            f"{risco_badge} {config['label']}",
            min_value=0.0,
            max_value=1_000_000_000.0,
            value=0.0,
            step=10_000.0,
            format="%.0f",
            key=f"cred_{cat_id}",
            help=f"{config['descricao']} | {config['base_legal']}",
        )
        if valor > 0:
            itens.append(ItemAquisicao(categoria=cat_id, valor_mensal=valor))

    if not st.button("Mapear créditos", type="primary"):
        return

    if not itens:
        st.warning("Informe ao menos uma categoria de aquisição.")
        return

    resultado = mapear_creditos(itens)

    st.divider()
    st.subheader("Mapa de Créditos")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Aquisições/mês", formatar_brl(resultado.total_aquisicoes_mensal))
    col2.metric("Créditos Estimados/mês", formatar_brl(resultado.total_credito_mensal))
    col3.metric("Créditos Estimados/ano", formatar_brl(resultado.total_credito_anual))

    if resultado.oportunidade_capex > 0:
        col4.metric(
            "Nova Oportunidade CAPEX/mês",
            formatar_brl(resultado.oportunidade_capex),
            delta="Crédito novo vs. regime anterior",
            delta_color="normal",
        )
    else:
        col4.metric("Créditos em Risco/mês", formatar_brl(resultado.creditos_em_risco))

    # Tabela detalhada
    rows = []
    for r in resultado.itens:
        rows.append({
            "Categoria": r.label,
            "Creditamento": _TIPO_BADGE.get(r.creditamento, r.creditamento),
            "Aquisição/mês": formatar_brl(r.valor_aquisicao_mensal),
            "Crédito/mês": formatar_brl(r.credito_estimado_mensal),
            "Crédito/ano": formatar_brl(r.credito_estimado_anual),
            "Base Legal": r.base_legal,
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Alertas
    if resultado.alertas:
        st.subheader("Alertas")
        for alerta in resultado.alertas:
            st.warning(alerta)

    # Alerta de restituição
    if resultado.total_credito_mensal > 0:
        st.info(
            f"**Restituição:** saldo credor acumulado por mais de "
            f"{resultado.prazo_restituicao_dias} dias gera direito a pedido de "
            f"restituição junto ao CGIBS (IBS) e RFB (CBS). "
            f"Monitore o prazo de acumulação."
        )

    # Ressalvas
    with st.expander("Ressalvas e limitações"):
        for r in resultado.itens:
            if r.ressalvas:
                st.caption(f"**{r.label}:**")
                for res in r.ressalvas:
                    st.caption(f"  • {res}")
        st.caption(
            "Créditos estimados com alíquotas de referência IBS+CBS (26,5%). "
            "Valores definitivos dependem de regulamentação do CGIBS. "
            "Não constitui escrituração fiscal."
        )
