"""
src/email_service.py — Serviço de envio de e-mails transacionais via SMTP.

Usa smtplib (stdlib Python) — zero dependência nova.
Configurado via variáveis de ambiente:
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, APP_URL

Se vars ausentes: loga warning e retorna sem erro (dev-safe).
"""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

_SMTP_HOST = os.getenv("SMTP_HOST", "")
_SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
_SMTP_USER = os.getenv("SMTP_USER", "")
_SMTP_PASS = os.getenv("SMTP_PASS", "")
_SMTP_FROM = os.getenv("SMTP_FROM", "Tribus-AI <noreply@tribus-ai.com.br>")
_APP_URL   = os.getenv("APP_URL", "http://localhost:3000")


def _smtp_configurado() -> bool:
    return bool(_SMTP_HOST and _SMTP_USER and _SMTP_PASS)


def _enviar(destinatario: str, assunto: str, html: str) -> None:
    """Envia e-mail HTML via SMTP com STARTTLS."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"]    = _SMTP_FROM
    msg["To"]      = destinatario
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT, timeout=10) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(_SMTP_USER, _SMTP_PASS)
        smtp.sendmail(_SMTP_FROM, destinatario, msg.as_string())


def enviar_email_confirmacao(email: str, nome: str, token: str) -> None:
    """
    Envia e-mail de confirmação de cadastro com link de verificação.

    Args:
        email : E-mail do destinatário
        nome  : Nome do usuário para personalização
        token : UUID de verificação
    """
    if not _smtp_configurado():
        logger.warning(
            "SMTP não configurado — e-mail de confirmação não enviado para %s. "
            "Configure SMTP_HOST, SMTP_USER e SMTP_PASS para ativar o envio.",
            email,
        )
        return

    link = f"{_APP_URL}/verify-email?token={token}"
    primeiro_nome = nome.split()[0] if nome else "usuário"

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 0">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)">

        <!-- Cabeçalho -->
        <tr>
          <td style="background:#1a2f4e;padding:32px 40px;text-align:center">
            <span style="font-size:22px;font-weight:800;color:#ffffff;letter-spacing:-0.5px">
              Tribus<span style="color:#3B9EE8">AI</span>
            </span>
            <p style="margin:4px 0 0;font-size:11px;color:rgba(255,255,255,.55);
                      letter-spacing:2px;text-transform:uppercase">
              Inteligência Tributária
            </p>
          </td>
        </tr>

        <!-- Corpo -->
        <tr>
          <td style="padding:40px 40px 32px">
            <h1 style="margin:0 0 16px;font-size:22px;color:#1a2f4e;font-weight:700">
              Confirme seu e-mail
            </h1>
            <p style="margin:0 0 12px;font-size:15px;color:#4a5568;line-height:1.6">
              Olá, <strong>{primeiro_nome}</strong>!
            </p>
            <p style="margin:0 0 28px;font-size:15px;color:#4a5568;line-height:1.6">
              Seu cadastro na Tribus-AI foi recebido. Clique no botão abaixo para confirmar
              seu e-mail e ativar seu período de teste gratuito de <strong>7 dias</strong>.
            </p>

            <!-- CTA -->
            <table cellpadding="0" cellspacing="0" style="margin:0 auto 28px">
              <tr>
                <td style="background:#2E75B6;border-radius:6px">
                  <a href="{link}"
                     style="display:inline-block;padding:14px 36px;font-size:15px;
                            font-weight:600;color:#ffffff;text-decoration:none;
                            letter-spacing:0.2px">
                    Confirmar e-mail
                  </a>
                </td>
              </tr>
            </table>

            <p style="margin:0 0 8px;font-size:13px;color:#718096;line-height:1.5">
              Ou copie e cole este link no navegador:
            </p>
            <p style="margin:0 0 28px;font-size:12px;color:#3B9EE8;word-break:break-all">
              {link}
            </p>

            <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 0 24px">
            <p style="margin:0;font-size:12px;color:#a0aec0;line-height:1.5">
              Se você não solicitou este cadastro, ignore este e-mail.
              Nenhuma ação é necessária da sua parte.
            </p>
          </td>
        </tr>

        <!-- Rodapé -->
        <tr>
          <td style="background:#f7fafc;padding:20px 40px;text-align:center;
                     border-top:1px solid #e2e8f0">
            <p style="margin:0;font-size:11px;color:#a0aec0">
              © 2026 Tribus-AI · Inteligência Tributária para a Reforma Tributária
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""

    try:
        _enviar(email, "Confirme seu e-mail — Tribus-AI", html)
        logger.info("E-mail de confirmação enviado para %s", email)
    except Exception as e:
        logger.error("Falha ao enviar e-mail de confirmação para %s: %s", email, e)
