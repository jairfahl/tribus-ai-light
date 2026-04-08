"""
ui/components/qualificacao_fatica.py — Componente Streamlit de Qualificação Fática.

G23: Coleta fatos do cliente e exibe semáforo de completude antes da análise.
Reutilizável no P1 do Protocolo e na Aba Consultar.
"""

import streamlit as st

from src.cognitive.qualificacao_fatica import (
    CAMPOS_BASE,
    CAMPOS_CREDITAMENTO,
    CAMPOS_SPLIT_PAYMENT,
    CAMPOS_TRANSICAO,
    calcular_semaforo,
)


def coletar_qualificacao_fatica(
    tipo_decisao: str = "geral",
    key_prefix: str = "qf",
    valores_iniciais: dict | None = None,
) -> dict:
    """
    Exibe formulário de qualificação fática e retorna fatos coletados.

    Args:
        tipo_decisao: 'geral' | 'creditamento' | 'split_payment' | 'transicao'
        key_prefix: prefixo para evitar colisão de keys Streamlit em múltiplos formulários
        valores_iniciais: dicionário com valores pré-preenchidos (ex: restaurar do banco)

    Returns:
        dict com os fatos coletados (apenas campos com valor preenchido)
    """
    ini = valores_iniciais or {}

    st.markdown("**🏢 Qualificação Fática**")
    st.caption(
        "Quanto mais contexto você fornecer, mais precisa será a análise. "
        "Campos com ✱ são obrigatórios para análise customizada."
    )

    fatos: dict = {}

    # ── BASE UNIVERSAL ────────────────────────────────────────────────────────
    with st.expander("📋 Dados da empresa (base universal)", expanded=True):

        fatos["cnae_principal"] = st.text_input(
            "CNAE Principal ✱",
            value=ini.get("cnae_principal", ""),
            placeholder=CAMPOS_BASE["cnae_principal"]["placeholder"],
            help=CAMPOS_BASE["cnae_principal"]["help"],
            key=f"{key_prefix}_cnae",
        )

        _regimes = [""] + CAMPOS_BASE["regime_tributario"]["opcoes"]
        _regime_idx = (
            _regimes.index(ini["regime_tributario"])
            if ini.get("regime_tributario") in _regimes
            else 0
        )
        fatos["regime_tributario"] = st.selectbox(
            "Regime Tributário ✱",
            options=_regimes,
            index=_regime_idx,
            help=CAMPOS_BASE["regime_tributario"]["help"],
            key=f"{key_prefix}_regime",
        )

        fatos["ufs_operacao"] = st.text_input(
            "UFs de Operação ✱",
            value=ini.get("ufs_operacao", ""),
            placeholder=CAMPOS_BASE["ufs_operacao"]["placeholder"],
            help=CAMPOS_BASE["ufs_operacao"]["help"],
            key=f"{key_prefix}_ufs",
        )

        _tipos = [""] + CAMPOS_BASE["tipo_operacao"]["opcoes"]
        _tipo_idx = (
            _tipos.index(ini["tipo_operacao"])
            if ini.get("tipo_operacao") in _tipos
            else 0
        )
        fatos["tipo_operacao"] = st.selectbox(
            "Tipo de Operação Predominante ✱",
            options=_tipos,
            index=_tipo_idx,
            help=CAMPOS_BASE["tipo_operacao"]["help"],
            key=f"{key_prefix}_tipo_op",
        )

        _faixas = [""] + CAMPOS_BASE["faturamento_faixa"]["opcoes"]
        _faixa_idx = (
            _faixas.index(ini["faturamento_faixa"])
            if ini.get("faturamento_faixa") in _faixas
            else 0
        )
        fatos["faturamento_faixa"] = st.selectbox(
            "Faturamento Bruto Anual ✱",
            options=_faixas,
            index=_faixa_idx,
            help=CAMPOS_BASE["faturamento_faixa"]["help"],
            key=f"{key_prefix}_faturamento",
        )

    # ── CAMPOS ADICIONAIS POR TIPO ────────────────────────────────────────────
    if tipo_decisao == "creditamento":
        with st.expander("📦 Dados de creditamento IBS/CBS"):
            for campo, config in CAMPOS_CREDITAMENTO.items():
                if "opcoes" in config:
                    _opts = [""] + config["opcoes"]
                    fatos[campo] = st.selectbox(
                        config["label"],
                        options=_opts,
                        index=_opts.index(ini[campo]) if ini.get(campo) in _opts else 0,
                        key=f"{key_prefix}_{campo}",
                    )
                else:
                    fatos[campo] = st.text_input(
                        config["label"],
                        value=ini.get(campo, ""),
                        placeholder=config.get("placeholder", ""),
                        key=f"{key_prefix}_{campo}",
                    )

    elif tipo_decisao == "split_payment":
        with st.expander("💳 Dados de split payment"):
            for campo, config in CAMPOS_SPLIT_PAYMENT.items():
                fatos[campo] = st.text_input(
                    config["label"],
                    value=ini.get(campo, ""),
                    placeholder=config.get("placeholder", ""),
                    key=f"{key_prefix}_{campo}",
                )

    elif tipo_decisao == "transicao":
        with st.expander("📅 Dados de transição"):
            for campo, config in CAMPOS_TRANSICAO.items():
                _opts = [""] + config["opcoes"]
                fatos[campo] = st.selectbox(
                    config["label"],
                    options=_opts,
                    index=_opts.index(ini[campo]) if ini.get(campo) in _opts else 0,
                    key=f"{key_prefix}_{campo}",
                )

    # ── SEMÁFORO ──────────────────────────────────────────────────────────────
    resultado = calcular_semaforo(fatos)

    if resultado.semaforo == "verde":
        st.success(resultado.mensagem)
    elif resultado.semaforo == "amarelo":
        st.warning(resultado.mensagem)
        if resultado.campos_faltando:
            st.caption(f"Campos faltando: {', '.join(resultado.campos_faltando)}")
    else:
        st.error(resultado.mensagem)
        if resultado.campos_faltando:
            st.caption(f"Campos obrigatórios ausentes: {', '.join(resultado.campos_faltando)}")

    # Persistir semáforo e fatos na sessão para uso no endpoint de análise
    st.session_state[f"{key_prefix}_semaforo"] = resultado.semaforo
    fatos_preenchidos = {k: v for k, v in fatos.items() if v and str(v).strip()}
    st.session_state[f"{key_prefix}_fatos"] = fatos_preenchidos

    return fatos_preenchidos
