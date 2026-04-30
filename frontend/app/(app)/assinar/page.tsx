"use client";
import { useState } from "react";
import { CheckCircle, CreditCard, Smartphone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/shared/Card";
import { useAuthStore } from "@/store/auth";
import api from "@/lib/api";

const BENEFICIOS = [
  "1 usuário ativo (acesso exclusivo por dispositivo)",
  "Mapa de decisão com 6 passos auditáveis",
  "Respostas jurídicas precisas com indicação da lei consultada",
  "Simuladores tributários (IBS, CBS, Split Payment)",
  "Outputs acionáveis em 5 formatos",
  "Histórico completo de consultas e decisões",
];

/** Formata CPF (000.000.000-00) ou CNPJ (00.000.000/0001-00) enquanto o usuário digita */
function formatarDocumento(raw: string): string {
  const d = raw.replace(/\D/g, "").slice(0, 14);
  if (d.length <= 11) {
    return d
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  }
  return d
    .replace(/(\d{2})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1/$2")
    .replace(/(\d{4})(\d{1,2})$/, "$1-$2");
}

export default function AssinarPage() {
  const { user } = useAuthStore();
  const [billingType, setBillingType] = useState<"CREDIT_CARD" | "PIX">("PIX");
  const [documento, setDocumento] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [erroDocumento, setErroDocumento] = useState("");

  const isTrial = !user?.subscription_status || user.subscription_status === "trial";

  const handleDocumento = (v: string) => {
    setDocumento(formatarDocumento(v));
    setErroDocumento("");
  };

  const onAssinar = async () => {
    if (!user?.tenant_id) {
      setErro("Tenant não identificado. Entre em contato com o suporte.");
      return;
    }

    const digits = documento.replace(/\D/g, "");
    if (digits.length !== 11 && digits.length !== 14) {
      setErroDocumento("Informe um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.");
      return;
    }

    setLoading(true);
    setErro("");
    setErroDocumento("");
    try {
      const res = await api.post<{ invoice_url: string; valor: number; desconto_percentual: number }>(
        "/v1/billing/subscribe",
        { tenant_id: user.tenant_id, billing_type: billingType, cpf_cnpj: digits }
      );
      if (res.data.invoice_url) {
        window.location.href = res.data.invoice_url;
      } else {
        setErro("Não foi possível gerar o link de pagamento. Tente novamente.");
      }
    } catch (err: unknown) {
      const axiosErr = err as { response?: { status?: number; data?: { detail?: string } } };
      const detail = axiosErr.response?.data?.detail ?? "";
      if (axiosErr.response?.status === 409) {
        setErro("Você já possui uma assinatura ativa. Entre em contato com o suporte.");
      } else if (detail === "cpf_cnpj_required" || detail === "cpf_cnpj_invalido") {
        setErroDocumento("CPF/CNPJ inválido ou não reconhecido. Verifique o número e tente novamente.");
      } else if (axiosErr.response?.status === 502) {
        setErro("O serviço de pagamento está temporariamente indisponível. Tente novamente em instantes.");
      } else {
        setErro("Erro ao processar assinatura. Tente novamente em instantes.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-10">
      {/* Badge trial */}
      {isTrial && user?.trial_ends_at && (
        <div
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-6"
          style={{ background: "rgba(59,130,246,.10)", border: "1px solid rgba(59,130,246,.25)", color: "#2563eb" }}
        >
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 shrink-0" />
          Trial ativo
        </div>
      )}

      <h1 className="text-2xl font-bold mb-1 text-foreground">Plano Starter</h1>
      <p className="text-sm mb-6 text-muted-foreground">
        Tudo que você precisa para decisões tributárias fundamentadas.
      </p>

      <Card>
        <div className="p-6">
          {/* Preço */}
          <div className="mb-6">
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-extrabold text-foreground">R$ 297</span>
              <span className="text-sm text-muted-foreground">/mês</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              nos 2 primeiros meses — depois{" "}
              <span className="font-semibold text-foreground">R$ 497/mês</span>
            </p>
          </div>

          {/* Benefícios */}
          <ul className="space-y-3 mb-8">
            {BENEFICIOS.map((b) => (
              <li key={b} className="flex items-center gap-2.5 text-sm text-foreground">
                <CheckCircle size={14} className="text-emerald-500 shrink-0" />
                {b}
              </li>
            ))}
          </ul>

          {/* CPF / CNPJ */}
          <div className="mb-5">
            <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5 text-foreground opacity-70">
              CPF ou CNPJ
            </label>
            <input
              type="text"
              inputMode="numeric"
              placeholder="000.000.000-00 ou 00.000.000/0001-00"
              value={documento}
              onChange={(e) => handleDocumento(e.target.value)}
              className="w-full h-10 px-3 rounded-lg border text-sm text-foreground bg-background outline-none focus:ring-2 focus:ring-primary/40 transition"
              style={{ borderColor: erroDocumento ? "#ef4444" : "var(--border)" }}
            />
            {erroDocumento && (
              <p className="text-xs mt-1.5" style={{ color: "#dc2626" }}>{erroDocumento}</p>
            )}
            <p className="text-xs text-muted-foreground mt-1.5">
              Usado pelo gateway de pagamento para identificar sua conta.
            </p>
          </div>

          {/* Forma de pagamento */}
          <p className="text-xs font-semibold uppercase tracking-wider mb-3 text-foreground opacity-70">
            Forma de pagamento
          </p>
          <div className="flex gap-3 mb-6">
            {(["PIX", "CREDIT_CARD"] as const).map((tipo) => (
              <button
                key={tipo}
                type="button"
                onClick={() => setBillingType(tipo)}
                className="flex-1 flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg border text-sm font-medium transition-all cursor-pointer"
                style={
                  billingType === tipo
                    ? { background: "#eff6ff", border: "1.5px solid #3b82f6", color: "#1d4ed8" }
                    : { background: "var(--card)", border: "1px solid var(--border)", color: "var(--muted-foreground)" }
                }
              >
                {tipo === "PIX" ? <Smartphone size={14} /> : <CreditCard size={14} />}
                {tipo === "PIX" ? "PIX" : "Cartão"}
              </button>
            ))}
          </div>

          {/* Erro geral */}
          {erro && (
            <div className="mb-4 p-3 rounded-lg" style={{ background: "#fef2f2", border: "1px solid #fecaca" }}>
              <p className="text-xs font-medium" style={{ color: "#dc2626" }}>{erro}</p>
            </div>
          )}

          <Button
            onClick={onAssinar}
            disabled={loading}
            className="w-full h-11 font-semibold text-white text-sm cursor-pointer"
            style={{
              background: "linear-gradient(135deg, #2E75B6 0%, #1F3864 100%)",
              boxShadow: "0 4px 14px rgba(30,77,150,.30)",
            }}
          >
            {loading ? "Processando…" : "Assinar agora"}
          </Button>

          <p className="text-center text-xs mt-4 text-muted-foreground">
            Você será redirecionado para a página de pagamento segura.
          </p>
        </div>
      </Card>

      <p className="text-center text-xs mt-6 text-muted-foreground">
        Dúvidas?{" "}
        <a
          href="https://wa.me/5511972521970?text=Ol%C3%A1%2C+acessei+o+Orbis.tax+e+tenho+interesse+em+saber+mais+do+app."
          target="_blank"
          rel="noopener noreferrer"
          className="underline"
        >
          Fale conosco no WhatsApp
        </a>
      </p>
    </div>
  );
}
