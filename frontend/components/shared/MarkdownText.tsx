"use client";
import React from "react";

/**
 * Renderiza texto com markdown mínimo: **negrito**, *itálico* e --- como separador.
 * Elimina os asteriscos e aplica formatação visual, preservando quebras de linha.
 */
function parseInline(text: string, keyPrefix: string): React.ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={`${keyPrefix}-${i}`}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith("*") && part.endsWith("*")) {
      return <em key={`${keyPrefix}-${i}`}>{part.slice(1, -1)}</em>;
    }
    return part;
  });
}

interface Props {
  text: string;
  className?: string;
}

export function MarkdownText({ text, className }: Props) {
  const lines = text.split("\n");
  return (
    <span className={className}>
      {lines.map((line, i) => (
        <React.Fragment key={i}>
          {line.trim() === "---"
            ? <hr className="border-border my-2" />
            : parseInline(line, String(i))
          }
          {i < lines.length - 1 && <br />}
        </React.Fragment>
      ))}
    </span>
  );
}
