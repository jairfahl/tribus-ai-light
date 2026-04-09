"""
Qualificação de Tenant — Progressive Profiling.
Insight E — Benchmarking Omnitax | GTM Abril 2026.

Coleta perfil do tenant em 3 momentos:
  Step 0 (cadastro):  tipo_atuacao, cargo_responsavel — obrigatórios
  Step 1 (dia 1-3):   regime_tributario, faturamento_faixa — opcionais
  Step 2 (dia 7):     erp_utilizado, dor_declarada — opcionais

Acesso ao produto nunca bloqueado por campos opcionais.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

import psycopg2
import streamlit as st

from src.db.pool import get_conn, put_conn

_BYPASS_UUID = "00000000-0000-0000-0000-000000000000"


# ── Persistência ──────────────────────────────────────────────────────────────

def salvar_perfil(user_id: str, campos: dict) -> bool:
    """Persiste campos de onboarding na tabela users."""
    if not user_id or not campos:
        return False
    conn = get_conn()
    try:
        set_parts = ", ".join(f"{k} = %s" for k in campos)
        valores = list(campos.values()) + [user_id]
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE users SET {set_parts} WHERE id = %s",
                    valores,
                )
        return True
    except Exception:
        return False
    finally:
        put_conn(conn)


def obter_step(user_id: str) -> int:
    """Retorna o onboarding_step atual do usuário."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT onboarding_step FROM users WHERE id = %s",
                (user_id,),
            )
            row = cur.fetchone()
            return row[0] if row else 0
    except Exception:
        return 0
    finally:
        put_conn(conn)


# ── Steps de onboarding ───────────────────────────────────────────────────────

def exibir_onboarding_step0(user_id: str) -> bool:
    """
    Campos obrigatórios — exibidos no primeiro acesso.
    Retorna True se preenchido e salvo (nunca retorna True diretamente —
    o st.rerun() é quem avança).
    """
    st.subheader("Antes de começar — dois campos rápidos")
    st.caption(
        "Essas informações personalizam sua experiência no Tribus-AI. "
        "Levam menos de 30 segundos."
    )

    tipo = st.selectbox(
        "Como você usa o Tribus-AI? ✱",
        ["", "Empresa (uso interno)", "Consultoria",
         "Escritório (contabilidade/advocacia)", "BPO Tributário"],
        key="ob_tipo_atuacao",
    )
    cargo = st.selectbox(
        "Qual é o seu cargo? ✱",
        ["", "Gestor / Gerente Tributário", "Analista Tributário", "Consultor",
         "Sócio / Diretor", "CFO / Controller", "Outro"],
        key="ob_cargo",
    )

    if st.button("Confirmar e entrar", type="primary"):
        if not tipo or not cargo:
            st.error("Preencha os dois campos para continuar.")
            return False
        ok = salvar_perfil(user_id, {
            "tipo_atuacao": tipo,
            "cargo_responsavel": cargo,
            "onboarding_step": 1,
        })
        if ok:
            st.session_state["onboarding_step"] = 1
            st.rerun()
        else:
            st.error("Erro ao salvar. Tente novamente.")
    return False


def exibir_onboarding_step1(user_id: str) -> None:
    """
    Campos opcionais — banner durante dias 1-3.
    Não bloqueia — o usuário pode dispensar.
    """
    with st.expander(
        "📋 Complete seu perfil (opcional — melhora suas sugestões)",
        expanded=False,
    ):
        st.caption("Dois campos opcionais para personalizar ainda mais sua experiência.")

        regime = st.selectbox(
            "Regime tributário predominante",
            ["", "Lucro Real", "Lucro Presumido", "Simples Nacional", "Misto", "N/A"],
            key="ob_regime",
        )
        faturamento = st.selectbox(
            "Faturamento anual (faixa)",
            ["", "Até R$ 30M", "R$ 30M – R$ 100M", "R$ 100M – R$ 350M",
             "Acima de R$ 350M", "N/A"],
            key="ob_faturamento",
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Salvar", key="ob_save_step1"):
                campos: dict = {}
                if regime:
                    campos["regime_tributario"] = regime
                if faturamento:
                    campos["faturamento_faixa"] = faturamento
                if campos:
                    campos["onboarding_step"] = 2
                    salvar_perfil(user_id, campos)
                    st.session_state["onboarding_step"] = 2
                    st.success("Perfil atualizado.")
                    st.rerun()
        with col2:
            if st.button("Agora não", key="ob_skip_step1"):
                salvar_perfil(user_id, {"onboarding_step": 2})
                st.session_state["onboarding_step"] = 2
                st.rerun()


def exibir_onboarding_step2(user_id: str) -> None:
    """
    Campos opcionais — exibidos a partir do dia 7.
    Não bloqueia — o usuário pode dispensar.
    """
    with st.expander(
        "💡 Uma última pergunta para personalizar suas análises",
        expanded=False,
    ):
        erp = st.text_input(
            "Qual ERP a empresa utiliza?",
            placeholder="Ex: SAP, TOTVS Protheus, Oracle, Sankhya, sem ERP...",
            max_chars=100,
            key="ob_erp",
        )
        dor = st.text_area(
            "Qual é a principal dificuldade tributária que você quer resolver?",
            placeholder="Ex: Entender o impacto do split payment na operação...",
            max_chars=280,
            height=80,
            key="ob_dor",
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Salvar", key="ob_save_step2"):
                campos: dict = {"onboarding_step": 3}
                if erp:
                    campos["erp_utilizado"] = erp
                if dor:
                    campos["dor_declarada"] = dor
                salvar_perfil(user_id, campos)
                st.session_state["onboarding_step"] = 3
                st.success("Perfil completo. Obrigado!")
                st.rerun()
        with col2:
            if st.button("Pular", key="ob_skip_step2"):
                salvar_perfil(user_id, {"onboarding_step": 3})
                st.session_state["onboarding_step"] = 3
                st.rerun()


# ── Ponto de entrada ──────────────────────────────────────────────────────────

def gerenciar_onboarding(user_id: str) -> bool:
    """
    Ponto de entrada principal. Chame em app.py após autenticação.

    Retorna True  → onboarding step 0 completo, app pode continuar.
    Retorna False → step 0 pendente, app deve chamar st.stop().
    """
    if not user_id or user_id == _BYPASS_UUID:
        return True

    step = st.session_state.get("onboarding_step")
    if step is None:
        step = obter_step(user_id)
        st.session_state["onboarding_step"] = step

    if step == 0:
        exibir_onboarding_step0(user_id)
        return False  # bloqueia o app

    if step == 1:
        exibir_onboarding_step1(user_id)  # banner opcional, não bloqueia

    if step == 2:
        # Exibir step 2 apenas após 7 dias do primeiro_uso
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT primeiro_uso FROM users WHERE id = %s",
                    (user_id,),
                )
                row = cur.fetchone()
                if row and row[0]:
                    dias = (datetime.now(timezone.utc) - row[0]).days
                    if dias >= 7:
                        exibir_onboarding_step2(user_id)
        except Exception:
            pass
        finally:
            put_conn(conn)

    return True  # step >= 1: acesso liberado
