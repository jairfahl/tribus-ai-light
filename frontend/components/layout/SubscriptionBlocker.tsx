"use client";
import { AlertTriangle } from "lucide-react";
import { useAuthStore } from "@/store/auth";

const BLOCKED_STATUSES = ["past_due", "canceled", "inactive"];

const MESSAGES: Record<string, { titulo: string; corpo: string }> = {
  past_due: {
    titulo: "Pagamento não identificado",
    corpo:
      "Não identificamos o pagamento de sua assinatura. Regularize para continuar consultando o Orbis.tax.",
  },
  canceled: {
    titulo: "Assinatura encerrada",
    corpo:
      "Sua assinatura foi cancelada. Para reativar o acesso, assine novamente.",
  },
  inactive: {
    titulo: "Acesso inativo",
    corpo:
      "Seu acesso está inativo. Assine um plano para continuar utilizando o Orbis.tax.",
  },
};

export function SubscriptionBlocker({ children }: { children: React.ReactNode }) {
  const { user } = useAuthStore();
  const status = user?.subscription_status ?? null;

  if (!status || !BLOCKED_STATUSES.includes(status)) {
    return <>{children}</>;
  }

  const msg = MESSAGES[status] ?? MESSAGES.inactive;

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
      <div
        className="w-full max-w-md rounded-xl p-6 text-center"
        style={{
          background: "var(--card)",
          border: "1px solid var(--border)",
          boxShadow: "var(--shadow-card)",
        }}
      >
        <div className="flex justify-center mb-4">
          <span
            className="inline-flex items-center justify-center w-12 h-12 rounded-full"
            style={{ background: "rgba(239,68,68,.10)" }}
          >
            <AlertTriangle size={24} style={{ color: "#ef4444" }} />
          </span>
        </div>

        <h2 className="text-lg font-bold text-foreground mb-2">{msg.titulo}</h2>
        <p className="text-sm text-muted-foreground mb-6">{msg.corpo}</p>

        <a
          href="/assinar"
          className="inline-flex items-center justify-center w-full h-11 rounded-lg font-semibold text-sm text-white cursor-pointer"
          style={{
            background: "linear-gradient(135deg, #2E75B6 0%, #1F3864 100%)",
            boxShadow: "0 4px 14px rgba(30,77,150,.30)",
          }}
        >
          Regularizar assinatura
        </a>

        <p className="text-xs text-muted-foreground mt-4">
          Dúvidas?{" "}
          <a
            href="https://wa.me/5511972521970?text=Ol%C3%A1%2C+preciso+de+ajuda+com+minha+assinatura+Orbis.tax."
            target="_blank"
            rel="noopener noreferrer"
            className="underline"
          >
            Fale conosco no WhatsApp
          </a>
        </p>
      </div>
    </div>
  );
}
