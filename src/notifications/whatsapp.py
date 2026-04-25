"""
src/notifications/whatsapp.py — Envio de mensagens WhatsApp via Evolution API.

Usado para notificações internas ao admin (ex: novo assinante confirmado).
Variáveis obrigatórias: EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE.
"""

import logging
import os

import httpx

logger = logging.getLogger(__name__)

EVOLUTION_API_URL      = os.getenv("EVOLUTION_API_URL", "")
EVOLUTION_API_KEY      = os.getenv("EVOLUTION_API_KEY", "")
EVOLUTION_INSTANCE     = os.getenv("EVOLUTION_INSTANCE", "")
ADMIN_WA_NUMBER        = "5511972521970"


def enviar_whatsapp_admin(mensagem: str) -> None:
    """
    Envia mensagem de texto para o número fixo do admin via Evolution API.
    Falha silenciosa com log de erro — nunca deve quebrar o fluxo principal.
    """
    if not all([EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE]):
        logger.warning("WhatsApp admin: variáveis Evolution API não configuradas — mensagem não enviada.")
        return

    url = f"{EVOLUTION_API_URL.rstrip('/')}/message/sendText/{EVOLUTION_INSTANCE}"
    payload = {
        "number": ADMIN_WA_NUMBER,
        "text":   mensagem,
    }
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}

    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        logger.info("WhatsApp admin enviado com sucesso para %s.", ADMIN_WA_NUMBER)
    except Exception as exc:
        logger.error("Erro ao enviar WhatsApp admin: %s", exc)
