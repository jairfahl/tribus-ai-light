"""
observability/budget_log.py — Context Budget Log para rastreamento de tokens.

Registra consumo de tokens por componente em cada análise, permitindo
diagnóstico de pressão de contexto (budget ESP-09: 12.100 tokens).
"""

import logging
from dataclasses import dataclass, field
from typing import Literal

logger = logging.getLogger(__name__)

ComponenteType = Literal[
    "system_prompt_summary",
    "system_prompt_full",
    "system_prompt_antialucinacao",
    "rag_chunks",
    "hyde_doc_hipotetico",
    "multi_query_variations",
    "step_back_query",
    "instrucoes_saida",
    "cot_instruction",
    "outros",
]


def contar_tokens(texto: str) -> int:
    """
    Contagem de tokens. Usa tiktoken se disponível, senão palavras * 1.3.
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(texto))
    except ImportError:
        return int(len(texto.split()) * 1.3)


@dataclass
class BudgetEntry:
    componente: ComponenteType
    descricao: str
    tokens: int


@dataclass
class ContextBudgetLog:
    prompt_codigo: str
    query_tipo: str
    budget_total: int = 12100
    entradas: list[BudgetEntry] = field(default_factory=list)

    def adicionar(self, componente: ComponenteType, descricao: str, tokens: int) -> None:
        self.entradas.append(BudgetEntry(componente, descricao, tokens))

    @property
    def total_usado(self) -> int:
        return sum(e.tokens for e in self.entradas)

    @property
    def budget_disponivel(self) -> int:
        return self.budget_total - self.total_usado

    @property
    def pressao_pct(self) -> float:
        """Percentual do budget utilizado. Alerta se > 85%."""
        if self.budget_total == 0:
            return 100.0
        return (self.total_usado / self.budget_total) * 100

    def alerta_pressao(self) -> bool:
        """True se uso > 85% do budget."""
        return self.pressao_pct > 85.0

    def to_log_string(self) -> str:
        """Gera string de log estruturado para persistência."""
        linhas = [
            f"[PROMPT:COMPOSE:START] {self.prompt_codigo} query_tipo={self.query_tipo}"
        ]
        for e in self.entradas:
            linhas.append(f"  [{e.componente.upper()}] {e.descricao} {e.tokens} tokens")
        linhas.append(
            f"[PROMPT:COMPOSE:COMPLETE] Total: {self.total_usado} tokens | "
            f"Budget disponivel: {self.budget_disponivel} tokens | "
            f"Pressao: {self.pressao_pct:.1f}%"
        )
        return "\n".join(linhas)
