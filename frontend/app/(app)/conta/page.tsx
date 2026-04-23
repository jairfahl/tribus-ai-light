"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { User, CreditCard, AlertTriangle, CheckCircle, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/shared/Card";
import { useAuthStore } from "@/store/auth";
import api from "@/lib/api";

const MOTIVOS = [
  "Preço elevado para minha realidade",
  "Não uso com frequência suficiente",
  "Encontrei outra solução",
  "Outro motivo",
] as const;

function StatusBadge({ status }: { status?: string | null }) {
  if (status === "active") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold"
            style={{ background: "rgba(16,185,129,.12)", color: "#059669", border: "1px solid rgba(16,185,129,.3)" }}>
        <CheckCircle size={11} /> Ativa
      </span>
    );
  }
  if (status === "trial") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold"
            style={{ background: "rgba(59,130,246,.12)", color: "#2563eb", border: "1px solid rgba(59,130,246,.3)" }}>
        <Clock size={11} /> Trial
      </span>
    );
  }
  if (status === "past_due") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold"
            style={{ background: "rgba(245,158,11,.12)", color: "#d97706", border: "1px solid rgba(245,158,11,.3)" }}>
        <AlertTriangle size={11} /> Pagamento pendente
      </span>
    );
  }
  if (status === "canceled") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold"
            style={{ background: "rgba(239,68,68,.10)", color: "#dc2626", border: "1px solid rgba(239,68,68,.3)" }}>
        Cancelada
      </span>
    );
  }
  return null;
}

function CancelModal({
  onConfirm,
  onClose,
  loading,
}: {
  onConfirm: (motivo: string) => void;
  onClose: () => void;
  loading: boolean;
}) {
  const [selected, setSelected] = useState<string>(MOTIVOS[0]);
  const [outro, setOutro] = useState("");

  const motivo = selected === "Outro motivo" ? (outro.trim() || "Outro motivo") : selected;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md mx-4 rounded-xl shadow-xl bg-card border border-border p-6">
        <h2 className="text-lg font-bold text-foreground mb-1">Cancelar assinatura</h2>
        <p className="text-sm text-muted-foreground mb-5">
          Lamentamos ver você partir. Antes de confirmar, nos conte o motivo:
        </p>

        <div className="space-y-2 mb-4">
          {MOTIVOS.map((m) => (
            <label key={m} className="flex items-center gap-3 cursor-pointer p-2.5 rounded-lg transition-colors hover:bg-muted">
              <input
                type="radio"
                name="motivo"
                value={m}
                checked={selected === m}
                onChange={() => setSelected(m)}
                className="accent-blue-600"
              />
              <span className="text-sm text-foreground">{m}</span>
            </label>
          ))}
        </div>

        {selected === "Outro motivo" && (
          <textarea
            value={outro}
            onChange={(e) => setOutro(e.target.value)}
            placeholder="Descreva brevemente o motivo..."
            rows={3}
            className="w-full mb-4 px-3 py-2 rounded-lg border border-border bg-background text-sm text-foreground resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )}

        <div className="flex gap-3 justify-end mt-2">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={loading}
            className="text-sm"
          >
            Voltar
          </Button>
          <Button
            onClick={() => onConfirm(motivo)}
            disabled={loading}
            className="text-sm text-white"
            style={{ background: "#dc2626" }}
          >
            {loading ? "Cancelando…" : "Confirmar cancelamento"}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function ContaPage() {
  const router = useRouter();
  const { user, token, setAuth } = useAuthStore();
  const [showModal, setShowModal] = useState(false);
  const [cancelLoading, setCancelLoading] = useState(false);
  const [erro, setErro] = useState("");

  if (!user) return null;

  const isActive = user.subscription_status === "active";

  const handleCancel = async (motivo: string) => {
    if (!user.tenant_id) return;
    setCancelLoading(true);
    setErro("");
    try {
      await api.post("/v1/billing/cancel", {
        tenant_id: user.tenant_id,
        motivo,
      });
      setAuth({ ...user, subscription_status: "canceled" }, token!);
      setShowModal(false);
      router.push("/assinar");
    } catch {
      setErro("Não foi possível cancelar a assinatura. Entre em contato pelo WhatsApp.");
    } finally {
      setCancelLoading(false);
    }
  };

  return (
    <>
      {showModal && (
        <CancelModal
          onConfirm={handleCancel}
          onClose={() => setShowModal(false)}
          loading={cancelLoading}
        />
      )}

      <div className="max-w-lg mx-auto px-4 py-10 space-y-6">
        <h1 className="text-2xl font-bold text-foreground">Minha Conta</h1>

        {/* Dados da conta */}
        <Card>
          <div className="p-6">
            <div className="flex items-center gap-3 mb-5">
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-white shrink-0"
                style={{ background: "linear-gradient(135deg,#2E75B6,#1F3864)" }}
              >
                {user.nome.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase()}
              </div>
              <div>
                <p className="font-semibold text-foreground">{user.nome}</p>
                <p className="text-sm text-muted-foreground">{user.email}</p>
              </div>
            </div>

            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-2 text-muted-foreground">
                <User size={14} />
                <span className="font-medium text-foreground">{user.perfil === "ADMIN" ? "Administrador" : "Usuário"}</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Status da assinatura */}
        <Card>
          <div className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <CreditCard size={16} className="text-muted-foreground" />
              <h2 className="text-sm font-semibold text-foreground uppercase tracking-wider">Assinatura</h2>
            </div>

            <div className="flex items-center justify-between flex-wrap gap-3">
              <div>
                <p className="font-semibold text-foreground">Plano Starter</p>
                {user.trial_ends_at && user.subscription_status === "trial" && (
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Trial até {new Date(user.trial_ends_at).toLocaleDateString("pt-BR")}
                  </p>
                )}
              </div>
              <StatusBadge status={user.subscription_status} />
            </div>

            {(user.subscription_status === "past_due" || user.subscription_status === "canceled" || user.subscription_status === "trial") && (
              <div className="mt-4 pt-4 border-t border-border">
                <Button
                  onClick={() => router.push("/assinar")}
                  className="w-full text-sm text-white font-semibold"
                  style={{ background: "linear-gradient(135deg,#2E75B6 0%,#1F3864 100%)" }}
                >
                  {user.subscription_status === "canceled" ? "Reativar assinatura" : "Assinar agora"}
                </Button>
              </div>
            )}
          </div>
        </Card>

        {/* Cancelamento — só para assinantes ativos */}
        {isActive && (
          <Card>
            <div className="p-6">
              <h2 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-2">Cancelar assinatura</h2>
              <p className="text-sm text-muted-foreground mb-4">
                Ao cancelar, seu acesso continua até o fim do período já pago.
              </p>

              {erro && (
                <div className="mb-4 p-3 rounded-lg tm-card-danger">
                  <p className="text-xs font-medium tm-text-danger">{erro}</p>
                </div>
              )}

              <Button
                variant="outline"
                onClick={() => setShowModal(true)}
                className="text-sm border-red-300 text-red-600 hover:bg-red-50"
              >
                Cancelar assinatura
              </Button>
            </div>
          </Card>
        )}
      </div>
    </>
  );
}
