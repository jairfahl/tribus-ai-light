"""
ui/components/sugestoes_proativas.py — Sugestões Proativas (DC v7, G25).
Exibição não intrusiva — expander colapsado por padrão.
"""

from __future__ import annotations

import streamlit as st

from src.cognitive.proatividade import (
    ativar_monitoramento_tema,
    gerar_sugestoes,
    silenciar_sugestao,
)


def exibir_sugestoes_proativas() -> None:
    """
    Exibe sugestões proativas baseadas no histórico do usuário.
    - Sem histórico suficiente: nada exibido
    - Com padrões detectados: expander colapsado (não intrusivo)
    """
    user_id = st.session_state.get("user_id")
    if not user_id:
        return

    try:
        sugestoes = gerar_sugestoes(user_id)
    except Exception:
        return

    if not sugestoes:
        return

    with st.expander(
        f"💡 {len(sugestoes)} sugestão(ões) baseada(s) no seu histórico",
        expanded=False,
    ):
        st.caption(
            "O Tribus-AI identificou padrões no seu uso e sugere ações proativas. "
            "Você pode ativar o monitoramento ou dispensar cada sugestão."
        )

        for sugestao in sugestoes:
            st.markdown(f"**{sugestao.tema_label}**")
            st.caption(sugestao.mensagem)
            st.caption(sugestao.acao_sugerida)

            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button(
                    "Ativar monitoramento",
                    key=f"ativar_{sugestao.tema}",
                ):
                    ativar_monitoramento_tema(user_id, sugestao.tema)
                    st.success(
                        f"Monitoramento de **{sugestao.tema_label}** ativado. "
                        "Você receberá alertas quando houver mudanças normativas."
                    )
                    st.rerun()

            with col2:
                if st.button(
                    "Dispensar (30 dias)",
                    key=f"silenciar_{sugestao.tema}",
                ):
                    silenciar_sugestao(user_id, sugestao.tema)
                    st.rerun()

            st.divider()
