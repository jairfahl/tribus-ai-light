"""
rag/ptf.py — Pre-filter Temporal (PTF).

Extrai data de referência da query e resolve o regime tributário
para injeção de cláusula WHERE antes da busca HNSW no pgvector.

Regimes:
  - vigente:    2024-01 a 2026-12 (PIS/COFINS atual)
  - transicao:  2027-01 a 2032-12 (IBS/CBS parcial)
  - definitivo: 2033-01 em diante (IBS/CBS pleno)
"""

import logging
import re
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)

# Mapeamento de regime por data
REGIME_MAP = [
    ("vigente",    date(2024, 1, 1), date(2026, 12, 31)),
    ("transicao",  date(2027, 1, 1), date(2032, 12, 31)),
    ("definitivo", date(2033, 1, 1), date(9999, 12, 31)),
]


def extrair_data_referencia(query: str) -> Optional[date]:
    """
    Extrai data de referência da query por heurística determinística (sem LLM).

    Padrões suportados:
      - "em 2028", "em 2033", "em janeiro de 2027"
      - "a partir de 2027", "no período de 2028 a 2030"
      - "exercício 2029", "ano fiscal 2028", "ano-calendário 2030"

    Returns:
        date: primeiro dia do ano identificado, ou None se sem referência temporal.
    """
    if not query:
        return None

    # Padrão: ano de 4 dígitos entre 2024 e 2049
    match = re.search(r'\b(20[2-4]\d)\b', query)
    if match:
        ano = int(match.group(1))
        if 2024 <= ano <= 2049:
            logger.info("PTF: data_referencia extraída — %d-01-01", ano)
            return date(ano, 1, 1)

    return None


def resolver_regime(data_ref: date) -> str:
    """Resolve regime tributário a partir da data de referência."""
    for regime, inicio, fim in REGIME_MAP:
        if inicio <= data_ref <= fim:
            return regime
    return "definitivo"


def is_future_scenario(data_ref: Optional[date]) -> bool:
    """True se data_referencia for posterior à data atual."""
    if data_ref is None:
        return False
    return data_ref > date.today()
