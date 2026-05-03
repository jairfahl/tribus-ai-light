"use client";
import { useState } from "react";
import { FileDown, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import axios from "axios";

interface ExportPDFButtonProps {
  sourceType: "analysis" | "dossie";
  sourceId?: string;
  analysisData?: Record<string, unknown>;
  className?: string;
  variant?: "default" | "outline" | "ghost";
  size?: "default" | "sm" | "lg" | "icon";
}

export function ExportPDFButton({
  sourceType,
  sourceId,
  analysisData,
  className,
  variant = "default",
  size = "sm",
}: ExportPDFButtonProps) {
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    setErro(false);
    try {
      const res = await api.post(
        "/v1/export/pdf",
        { source_type: sourceType, source_id: sourceId ?? null, analysis_data: analysisData ?? null },
        { responseType: "blob" }
      );
      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      const disposition: string = res.headers["content-disposition"] ?? "";
      const match = disposition.match(/filename=([^\s;]+)/);
      a.download = match ? match[1] : "orbis_documento.pdf";
      a.href = url;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e: unknown) {
      if (axios.isAxiosError(e) && e.response?.status === 429) {
        setErro(true);
      } else {
        setErro(true);
      }
      setTimeout(() => setErro(false), 4000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="inline-flex flex-col items-start gap-1">
      <Button
        variant={variant}
        size={size}
        onClick={handleExport}
        disabled={loading}
        className={`bg-primary text-primary-foreground hover:bg-primary/90 font-medium shadow-sm ${className ?? ""}`}
        title="Exportar como PDF"
      >
        {loading ? (
          <Loader2 size={14} className="animate-spin" />
        ) : (
          <FileDown size={14} />
        )}
        <span className="ml-1.5">{loading ? "Gerando…" : "Exportar PDF"}</span>
      </Button>
      {erro && (
        <p className="text-xs text-red-600">Não foi possível gerar o PDF. Tente novamente.</p>
      )}
    </div>
  );
}
