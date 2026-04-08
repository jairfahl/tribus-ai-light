"""
src/cognitive/qualificacao_fatica.py — Qualificação Fática Estruturada (DC v7, Eixo 3).

G23: Sem Qualificação Fática, a análise é genérica — baseada apenas na norma e em
interpretações abstratas. Com Qualificação Fática, a análise é customizada ao contexto
do cliente, permitindo recomendações específicas e quantificadas.

Semáforo de completude:
  🟢 Verde   — todos os 5 campos base preenchidos
  🟡 Amarelo — 3 ou 4 campos preenchidos (análise com ressalvas)
  🔴 Vermelho — menos de 3 campos (análise genérica, scoring rebaixado)
"""

from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# CAMPOS BASE UNIVERSAL (DC v7)
# ---------------------------------------------------------------------------

CAMPOS_BASE: dict[str, dict] = {
    "cnae_principal": {
        "label": "CNAE Principal",
        "obrigatorio": True,
        "placeholder": "Ex: 4711-3/02 — Comércio varejista de mercadorias em geral",
        "help": "CNAE da atividade econômica principal da empresa",
    },
    "regime_tributario": {
        "label": "Regime Tributário",
        "obrigatorio": True,
        "opcoes": ["Lucro Real", "Lucro Presumido", "Simples Nacional", "MEI"],
        "help": "Regime de apuração do IRPJ/CSLL vigente",
    },
    "ufs_operacao": {
        "label": "UFs de Operação",
        "obrigatorio": True,
        "placeholder": "Ex: SP (origem), RJ e MG (destino)",
        "help": "Estados onde a empresa opera — impacta alíquota IBS estadual",
    },
    "tipo_operacao": {
        "label": "Tipo de Operação Predominante",
        "obrigatorio": True,
        "opcoes": ["B2B", "B2C", "Intragrupo", "Exportação", "Misto"],
        "help": "Natureza das operações — impacta creditamento e split payment",
    },
    "faturamento_faixa": {
        "label": "Faturamento Bruto Anual (faixa)",
        "obrigatorio": True,
        "opcoes": [
            "Até R$ 4,8M (Simples)",
            "R$ 4,8M a R$ 50M",
            "R$ 50M a R$ 300M",
            "Acima de R$ 300M",
        ],
        "help": "Faixa de faturamento — impacta regime e elegibilidade a regimes especiais",
    },
}

# ---------------------------------------------------------------------------
# CAMPOS ADICIONAIS POR TIPO DE DECISÃO RT
# ---------------------------------------------------------------------------

CAMPOS_CREDITAMENTO: dict[str, dict] = {
    "insumos_principais": {
        "label": "Insumos principais na cadeia produtiva",
        "obrigatorio": False,
        "placeholder": "Ex: matérias-primas, embalagens, energia elétrica",
    },
    "fornecedores_simples": {
        "label": "Possui fornecedores no Simples Nacional?",
        "obrigatorio": False,
        "opcoes": ["Sim", "Não", "Não sei"],
    },
}

CAMPOS_SPLIT_PAYMENT: dict[str, dict] = {
    "mix_pagamento": {
        "label": "Mix de meios de pagamento",
        "obrigatorio": False,
        "placeholder": "Ex: 60% cartão crédito, 30% boleto, 10% PIX",
    },
    "prazo_medio_recebimento": {
        "label": "Prazo médio de recebimento (dias)",
        "obrigatorio": False,
        "placeholder": "Ex: 30",
    },
}

CAMPOS_TRANSICAO: dict[str, dict] = {
    "saldo_credor_icms": {
        "label": "Possui saldo credor de ICMS acumulado?",
        "obrigatorio": False,
        "opcoes": ["Sim", "Não", "Não sei"],
    },
}

# ---------------------------------------------------------------------------
# SEMÁFORO DE COMPLETUDE
# ---------------------------------------------------------------------------

@dataclass
class ResultadoQualificacao:
    semaforo: str                              # "verde" | "amarelo" | "vermelho"
    campos_preenchidos: int
    campos_obrigatorios: int
    campos_faltando: list[str] = field(default_factory=list)
    mensagem: str = ""


def calcular_semaforo(fatos: dict) -> ResultadoQualificacao:
    """
    Calcula o semáforo de completude fática.

    Regras:
      Verde   — todos os 5 obrigatórios preenchidos
      Amarelo — 3 ou 4 obrigatórios preenchidos (análise prossegue com ressalvas)
      Vermelho — menos de 3 obrigatórios (análise genérica, scoring rebaixado)
    """
    obrigatorios = [k for k, v in CAMPOS_BASE.items() if v["obrigatorio"]]
    preenchidos = [k for k in obrigatorios if fatos.get(k, "").strip()]
    faltando = [CAMPOS_BASE[k]["label"] for k in obrigatorios if k not in preenchidos]

    n_preenchidos = len(preenchidos)
    n_obrigatorios = len(obrigatorios)

    if n_preenchidos == n_obrigatorios:
        semaforo = "verde"
        mensagem = "✅ Qualificação fática completa — análise customizada ao contexto."
    elif n_preenchidos >= 3:
        semaforo = "amarelo"
        mensagem = (
            f"🟡 Qualificação fática parcial ({n_preenchidos}/{n_obrigatorios} campos). "
            "A análise prosseguirá com ressalvas explícitas."
        )
    else:
        semaforo = "vermelho"
        mensagem = (
            f"🔴 Qualificação fática insuficiente ({n_preenchidos}/{n_obrigatorios} campos). "
            "A análise será genérica e o scoring de confiança será rebaixado."
        )

    return ResultadoQualificacao(
        semaforo=semaforo,
        campos_preenchidos=n_preenchidos,
        campos_obrigatorios=n_obrigatorios,
        campos_faltando=faltando,
        mensagem=mensagem,
    )


# ---------------------------------------------------------------------------
# INJEÇÃO NO CONTEXTO DO LLM
# ---------------------------------------------------------------------------

def formatar_fatos_para_contexto(fatos: dict) -> str:
    """
    Formata os fatos do cliente para injeção no contexto do LLM.

    Retorna bloco de texto a ser inserido no user_msg antes dos chunks legislativos.
    Quando vazio, sinaliza explicitamente que a análise é genérica.
    """
    if not fatos:
        return (
            "\n\nQUALIFICAÇÃO FÁTICA: Não fornecida. "
            "Análise genérica — sem customização ao contexto do cliente."
        )

    # Filtrar apenas campos com valor preenchido
    campos_com_valor = {k: v for k, v in fatos.items() if v and str(v).strip()}
    if not campos_com_valor:
        return (
            "\n\nQUALIFICAÇÃO FÁTICA: Não fornecida. "
            "Análise genérica — sem customização ao contexto do cliente."
        )

    _todos_campos = {**CAMPOS_BASE, **CAMPOS_CREDITAMENTO, **CAMPOS_SPLIT_PAYMENT, **CAMPOS_TRANSICAO}
    linhas = ["\n\nQUALIFICAÇÃO FÁTICA DO CLIENTE (use estes dados para customizar a análise):"]
    for campo, valor in campos_com_valor.items():
        label = _todos_campos.get(campo, {}).get("label", campo.replace("_", " ").capitalize())
        linhas.append(f"- {label}: {valor}")

    resultado = calcular_semaforo(fatos)
    if resultado.semaforo == "vermelho":
        linhas.append(
            "\n⚠ ATENÇÃO: Qualificação fática insuficiente. "
            "Reduza o scoring_confianca e indique na resposta que a análise é genérica."
        )
    elif resultado.semaforo == "amarelo":
        linhas.append(
            "\n⚠ ATENÇÃO: Qualificação fática parcial. "
            "Indique na resposta quais aspectos precisariam de mais dados para análise precisa."
        )

    return "\n".join(linhas)
