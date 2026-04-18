"use client";
import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Eye, EyeOff, ShieldCheck, Clock, Lock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import api from "@/lib/api";

const schema = z.object({
  nome:         z.string().min(2, "Nome deve ter ao menos 2 caracteres"),
  email:        z.string().email("E-mail inválido"),
  senha:        z.string().min(6, "Senha deve ter ao menos 6 caracteres"),
  razao_social: z.string().min(2, "Informe o nome da empresa"),
  cnpj_raiz:    z.string().regex(/^\d{8}$/, "CNPJ raiz deve ter 8 dígitos numéricos").optional().or(z.literal("")),
  lgpd_consent: z.boolean().refine((v) => v === true, {
    message: "O consentimento é obrigatório para o cadastro.",
  }),
});
type Form = z.infer<typeof schema>;

const BULLETS = [
  {
    icon: <Clock size={16} className="text-blue-300" />,
    text: "7 dias grátis — sem cartão de crédito",
  },
  {
    icon: <ShieldCheck size={16} className="text-blue-300" />,
    text: "Corpus curado da Reforma Tributária LC 214/2025",
  },
  {
    icon: <Lock size={16} className="text-blue-300" />,
    text: "Dados protegidos pela LGPD · Sem compartilhamento",
  },
];

export default function RegisterPage() {
  const [showPass, setShowPass] = useState(false);
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<Form>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: Form) => {
    setErro("");
    try {
      await api.post("/v1/auth/register", {
        nome:         data.nome,
        email:        data.email,
        senha:        data.senha,
        razao_social: data.razao_social,
        cnpj_raiz:    data.cnpj_raiz || undefined,
        lgpd_consent: data.lgpd_consent,
      });
      setSucesso(true);
    } catch (err: unknown) {
      const status = (err as { response?: { status?: number; data?: { detail?: string } } })?.response?.status;
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      if (status === 409) {
        setErro(detail ?? "E-mail ou CNPJ já cadastrado.");
      } else {
        setErro(detail ?? "Erro ao realizar cadastro. Tente novamente.");
      }
    }
  };

  return (
    <div className="min-h-screen flex">

      {/* ── PAINEL ESQUERDO ───────────────────────────────────────── */}
      <div
        className="hidden lg:flex flex-col justify-between px-14 py-12 w-[46%] relative overflow-hidden"
        style={{ background: "linear-gradient(155deg, #1e4d96 0%, #1F3864 55%, #0e1f3a 100%)" }}
      >
        <div
          className="absolute -top-40 -right-40 w-[480px] h-[480px] rounded-full"
          style={{ background: "radial-gradient(circle, rgba(96,165,250,0.12) 0%, transparent 70%)" }}
        />
        <div
          className="absolute bottom-0 left-0 w-[340px] h-[340px] rounded-full"
          style={{ background: "radial-gradient(circle, rgba(147,197,253,0.07) 0%, transparent 70%)" }}
        />

        {/* Logo */}
        <div className="relative">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo.png" alt="Tribus-AI" style={{ width: "180px", height: "auto" }} />
        </div>

        {/* Conteúdo central */}
        <div className="relative">
          <div
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-8"
            style={{ background: "rgba(255,255,255,0.10)", color: "rgba(255,255,255,0.75)" }}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" />
            Trial gratuito · 7 dias · Sem cartão
          </div>

          <h1 className="text-[2.6rem] font-extrabold text-white leading-[1.15] mb-5 tracking-tight">
            Comece agora<br />e domine a<br />
            <span style={{ color: "rgba(147,197,253,0.9)" }}>Reforma Tributária.</span>
          </h1>

          <p className="text-base mb-10 max-w-[320px] leading-relaxed" style={{ color: "rgba(255,255,255,0.55)" }}>
            Crie sua conta em menos de 1 minuto e acesse o protocolo cognitivo P1→P6 com corpus curado e trilha de auditoria.
          </p>

          <ul className="space-y-4">
            {BULLETS.map(({ icon, text }) => (
              <li key={text} className="flex items-start gap-3">
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
                  style={{ background: "rgba(255,255,255,0.10)" }}
                >
                  {icon}
                </div>
                <span className="text-sm leading-snug" style={{ color: "rgba(255,255,255,0.72)" }}>
                  {text}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <p className="relative text-xs" style={{ color: "rgba(255,255,255,0.25)" }}>
          © 2026 Tribus-AI · Não constitui parecer jurídico
        </p>
      </div>

      {/* ── PAINEL DIREITO ────────────────────────────────────────── */}
      <div className="flex-1 flex items-center justify-center p-8" style={{ background: "#f1f5f9" }}>
        <div className="w-full max-w-[440px]">

          {/* Logo mobile */}
          <div className="lg:hidden mb-8 text-center">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/logo.png" alt="Tribus-AI" style={{ height: "36px", width: "auto", margin: "0 auto 8px" }} />
            <p className="text-sm text-slate-500">7 dias grátis · sem cartão</p>
          </div>

          {/* Card */}
          <div
            className="rounded-2xl p-8"
            style={{
              background: "#ffffff",
              boxShadow: "0 4px 32px rgba(15,32,68,0.10), 0 1px 4px rgba(15,32,68,0.06)",
              border: "1px solid rgba(226,232,240,0.8)",
            }}
          >
            {sucesso ? (
              /* ── Estado de sucesso ── */
              <div className="text-center py-4">
                <div
                  className="w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-4"
                  style={{ background: "#dcfce7" }}
                >
                  <ShieldCheck size={26} style={{ color: "#16a34a" }} />
                </div>
                <h2 className="text-xl font-bold mb-2" style={{ color: "#0f2040" }}>
                  Cadastro realizado!
                </h2>
                <p className="text-sm mb-6" style={{ color: "#64748b" }}>
                  Enviamos um e-mail de confirmação para o endereço informado.
                  Verifique sua caixa de entrada (e spam) e clique no link para ativar sua conta.
                </p>
                <Link
                  href="/login"
                  className="text-sm font-semibold"
                  style={{ color: "#2E75B6" }}
                >
                  Voltar para o login →
                </Link>
              </div>
            ) : (
              /* ── Formulário ── */
              <>
                <div className="mb-6">
                  <h2 className="text-2xl font-bold mb-1" style={{ color: "#0f2040" }}>
                    Criar conta grátis
                  </h2>
                  <p className="text-sm" style={{ color: "#64748b" }}>
                    7 dias de trial · sem cartão de crédito
                  </p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                  {/* Nome */}
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "#475569" }}>
                      Nome completo
                    </label>
                    <Input
                      {...register("nome")}
                      type="text"
                      placeholder="João da Silva"
                      className="h-11 bg-slate-50 border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500/20"
                      autoComplete="name"
                    />
                    {errors.nome && <p className="text-xs text-red-500 mt-1">{errors.nome.message}</p>}
                  </div>

                  {/* E-mail */}
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "#475569" }}>
                      E-mail
                    </label>
                    <Input
                      {...register("email")}
                      type="email"
                      placeholder="joao@empresa.com.br"
                      className="h-11 bg-slate-50 border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500/20"
                      autoComplete="email"
                    />
                    {errors.email && <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>}
                  </div>

                  {/* Senha */}
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "#475569" }}>
                      Senha
                    </label>
                    <div className="relative">
                      <Input
                        {...register("senha")}
                        type={showPass ? "text" : "password"}
                        placeholder="Mínimo 6 caracteres"
                        className="h-11 bg-slate-50 border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500/20 pr-11"
                        autoComplete="new-password"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPass(!showPass)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors cursor-pointer"
                        aria-label={showPass ? "Ocultar senha" : "Mostrar senha"}
                      >
                        {showPass ? <EyeOff size={15} /> : <Eye size={15} />}
                      </button>
                    </div>
                    {errors.senha && <p className="text-xs text-red-500 mt-1">{errors.senha.message}</p>}
                  </div>

                  {/* Empresa */}
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "#475569" }}>
                      Empresa (Razão Social)
                    </label>
                    <Input
                      {...register("razao_social")}
                      type="text"
                      placeholder="Empresa Ltda."
                      className="h-11 bg-slate-50 border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500/20"
                      autoComplete="organization"
                    />
                    {errors.razao_social && <p className="text-xs text-red-500 mt-1">{errors.razao_social.message}</p>}
                  </div>

                  {/* CNPJ (opcional) */}
                  <div>
                    <label className="block text-xs font-semibold uppercase tracking-wider mb-1.5" style={{ color: "#475569" }}>
                      CNPJ Raiz <span className="font-normal normal-case" style={{ color: "#94a3b8" }}>(8 dígitos, opcional)</span>
                    </label>
                    <Input
                      {...register("cnpj_raiz")}
                      type="text"
                      placeholder="12345678"
                      maxLength={8}
                      className="h-11 bg-slate-50 border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500/20"
                    />
                    {errors.cnpj_raiz && <p className="text-xs text-red-500 mt-1">{errors.cnpj_raiz.message}</p>}
                  </div>

                  {/* Checkbox LGPD */}
                  <div className="flex items-start gap-3 pt-1">
                    <input
                      {...register("lgpd_consent")}
                      type="checkbox"
                      id="lgpd"
                      className="mt-0.5 w-4 h-4 rounded border-slate-300 accent-blue-600 cursor-pointer shrink-0"
                    />
                    <label htmlFor="lgpd" className="text-xs leading-relaxed cursor-pointer" style={{ color: "#64748b" }}>
                      Concordo em receber comunicações da Tribus-AI e autorizo o uso dos meus dados
                      conforme a{" "}
                      <span className="font-semibold" style={{ color: "#2E75B6" }}>LGPD (Lei 13.709/2018)</span>.
                    </label>
                  </div>
                  {errors.lgpd_consent && (
                    <p className="text-xs text-red-500 -mt-2">{errors.lgpd_consent.message}</p>
                  )}

                  {/* Erro geral */}
                  {erro && (
                    <div className="p-3 rounded-lg" style={{ background: "#fef2f2", border: "1px solid #fecaca" }}>
                      <p className="text-xs font-medium" style={{ color: "#dc2626" }}>{erro}</p>
                    </div>
                  )}

                  <Button
                    type="submit"
                    className="w-full h-11 font-semibold text-white text-sm mt-1 cursor-pointer"
                    style={{
                      background: "linear-gradient(135deg, #2E75B6 0%, #1F3864 100%)",
                      boxShadow: "0 4px 14px rgba(30,77,150,0.35)",
                    }}
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? "Criando conta…" : "Criar conta grátis"}
                  </Button>
                </form>

                <p className="text-center text-xs mt-5" style={{ color: "#94a3b8" }}>
                  Já tem conta?{" "}
                  <Link href="/login" className="font-semibold" style={{ color: "#2E75B6" }}>
                    Entrar
                  </Link>
                </p>
              </>
            )}
          </div>

          <p className="text-center text-xs mt-6" style={{ color: "#94a3b8" }}>
            Tribus-AI © 2026 · Não constitui parecer jurídico
          </p>
        </div>
      </div>
    </div>
  );
}
