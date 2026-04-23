import Link from "next/link";

export const metadata = {
  title: "Termos de Uso — Orbis.tax",
  description: "Termos de Uso da plataforma Orbis.tax. Versão 1.0 — Abril 2026.",
};

export default function TermosDeUsoPage() {
  return (
    <div style={{ background: "#f4f6f9", minHeight: "100vh", fontFamily: "'Segoe UI', Arial, sans-serif" }}>

      {/* Header */}
      <header style={{ background: "#1a2f4e", padding: "20px 40px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <Link href="/" style={{ textDecoration: "none" }}>
          <span style={{ fontSize: 20, fontWeight: 800, color: "#fff", letterSpacing: "-0.5px" }}>
            Orbis<span style={{ color: "#3B9EE8" }}>.tax</span>
          </span>
        </Link>
        <Link
          href="/login"
          style={{ fontSize: 13, color: "rgba(255,255,255,.70)", textDecoration: "none" }}
        >
          Entrar na plataforma →
        </Link>
      </header>

      {/* Conteúdo */}
      <main style={{ maxWidth: 800, margin: "0 auto", padding: "48px 24px 80px" }}>

        {/* Título */}
        <div style={{ marginBottom: 40 }}>
          <p style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#3B9EE8", marginBottom: 8 }}>
            Versão 1.0 — Abril 2026
          </p>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "#1a2f4e", margin: "0 0 12px" }}>
            Termos de Uso da Plataforma
          </h1>
          <p style={{ fontSize: 15, color: "#4a5568", lineHeight: 1.7, margin: 0 }}>
            Leia atentamente antes de utilizar o Orbis.tax. O acesso ou uso da plataforma implica
            aceitação integral destes Termos.
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>

          {/* Seção 1 */}
          <Section titulo="1. Aceitação dos Termos">
            <p>
              Ao acessar ou utilizar a plataforma Orbis.tax, você (<strong>"Usuário"</strong> ou <strong>"Tenant"</strong>)
              concorda integralmente com estes Termos de Uso. Se você não concordar com qualquer disposição
              aqui contida, não utilize a plataforma.
            </p>
            <p>
              Estes Termos constituem contrato vinculante entre o Tenant e a empresa operadora do
              Orbis.tax (<strong>"Orbis.tax"</strong>, <strong>"nós"</strong>). A utilização da plataforma
              após o cadastro implica aceitação destes Termos.
            </p>
          </Section>

          {/* Seção 2 */}
          <Section titulo="2. Descrição do Serviço">
            <p>
              O Orbis.tax é uma plataforma SaaS de inteligência tributária baseada em inteligência
              artificial (RAG — Retrieval-Augmented Generation), desenvolvida para auxiliar profissionais
              tributários na navegação da Reforma Tributária brasileira (EC 132/2023, LC 214/2025,
              LC 227/2026) por meio de um protocolo estruturado de decisão de 6 passos (P1–P6).
            </p>
            <Callout>
              <strong>Disclaimer obrigatório de IA (§ 2.1):</strong> O Orbis.tax é uma ferramenta de
              apoio à decisão. <strong>Não substitui parecer jurídico, contábil ou de qualquer outro
              profissional habilitado.</strong> A responsabilidade pela decisão final é exclusivamente
              do Usuário.
            </Callout>
          </Section>

          {/* Seção 3 */}
          <Section titulo="3. Modelo de Cobrança e Trial">
            <h3 style={h3Style}>3.1 Período de Trial</h3>
            <p>
              Novos tenants têm acesso gratuito à plataforma por <strong>7 (sete) dias corridos</strong> a
              partir do cadastro. Após esse período, o acesso é condicionado à contratação de um plano pago.
            </p>

            <h3 style={h3Style}>3.2 Modelo MAU</h3>
            <p>
              A cobrança é baseada em <strong>MAU</strong> (Monthly Active Users — Usuários Ativos Mensais)
              por tenant. Define-se como usuário ativo aquele que realizou ao menos um login na plataforma
              no mês calendário de referência.
            </p>

            <h3 style={h3Style}>3.3 Planos</h3>
            <p>
              Os planos disponíveis, com suas respectivas características e valores, estão descritos na
              página de planos da plataforma. Os valores estão sujeitos a reajuste anual com aviso prévio
              de 30 dias.
            </p>

            <h3 style={h3Style}>3.4 Inadimplência</h3>
            <p>
              Em caso de inadimplência, o acesso à plataforma será suspenso após notificação. Os dados do
              tenant serão retidos por <strong>90 dias</strong> após o cancelamento, após o que poderão ser
              excluídos definitivamente.
            </p>
          </Section>

          {/* Seção 4 */}
          <Section titulo="4. Cancelamento">
            <p>
              O Tenant pode cancelar sua assinatura a qualquer momento pelo painel de administração. O
              cancelamento tem efeito ao final do período de cobrança em curso. Não há reembolso
              proporcional por período não utilizado, salvo disposição contrária em lei.
            </p>
          </Section>

          {/* Seção 5 */}
          <Section titulo="5. Responsabilidades do Usuário">
            <p>O Usuário compromete-se a:</p>
            <ul>
              <li>Manter suas credenciais de acesso em sigilo e notificar imediatamente o Orbis.tax em caso de uso não autorizado.</li>
              <li>Utilizar a plataforma exclusivamente para fins lícitos e relacionados à gestão tributária de sua organização.</li>
              <li>Não compartilhar acesso com terceiros não cadastrados como usuários do tenant.</li>
              <li>Verificar a atualidade e adequação das análises geradas pela IA antes de aplicá-las em decisões reais.</li>
              <li>Não utilizar a plataforma para gerar, armazenar ou processar informações de terceiros sem base legal adequada.</li>
            </ul>
          </Section>

          {/* Seção 6 */}
          <Section titulo="6. Limitação de Responsabilidade">
            <p>O Orbis.tax não se responsabiliza por:</p>
            <ul>
              <li>Decisões tributárias tomadas com base nos outputs da plataforma.</li>
              <li>Desatualização temporária do corpus em relação à legislação vigente.</li>
              <li>Interrupções de serviço decorrentes de manutenção programada ou causas de força maior.</li>
              <li>Danos indiretos, lucros cessantes ou danos emergentes decorrentes do uso ou impossibilidade de uso da plataforma.</li>
            </ul>
            <p>
              A responsabilidade total do Orbis.tax, em qualquer hipótese, fica limitada ao valor pago
              pelo Tenant nos últimos <strong>3 (três) meses</strong> de assinatura.
            </p>
          </Section>

          {/* Seção 7 */}
          <Section titulo="7. Propriedade Intelectual">
            <p>
              Todos os elementos da plataforma — interface, algoritmos, prompts, pipeline RAG, corpus
              curado e marca — são propriedade exclusiva do Orbis.tax e protegidos pela legislação de
              propriedade intelectual aplicável. É vedada qualquer cópia, engenharia reversa ou uso
              não autorizado.
            </p>
            <p>
              Os dados inseridos pelo Tenant na plataforma (cases, premissas, hipóteses, decisões) são
              de <strong>propriedade do Tenant</strong>. O Orbis.tax não utiliza dados de um tenant para
              gerar análises ou heurísticas para outro tenant.
            </p>
          </Section>

          {/* Seção 8 */}
          <Section titulo="8. Legal Hold">
            <p>
              O Tenant pode ativar <strong>Legal Hold</strong> sobre seus dados em caso de procedimento
              fiscal, administrativo ou judicial em curso ou iminente. Com o Legal Hold ativo, os dados
              protegidos não poderão ser excluídos ou alterados pelo sistema. O procedimento de ativação
              está disponível no painel de administração.
            </p>
          </Section>

          {/* Seção 9 */}
          <Section titulo="9. Alterações nos Termos">
            <p>
              O Orbis.tax pode alterar estes Termos a qualquer momento, com <strong>notificação prévia
              de 30 dias</strong> por e-mail ao administrador do tenant. O uso continuado da plataforma
              após esse prazo implica aceitação das alterações.
            </p>
          </Section>

          {/* Seção 10 */}
          <Section titulo="10. Foro e Lei Aplicável">
            <p>
              Estes Termos são regidos pela <strong>legislação brasileira</strong>. Fica eleito o foro
              da <strong>Comarca de Indaiatuba/SP</strong> para dirimir quaisquer controvérsias, com
              renúncia a qualquer outro, por mais privilegiado que seja.
            </p>
          </Section>

        </div>

        {/* Rodapé */}
        <div style={{ marginTop: 48, paddingTop: 24, borderTop: "1px solid #e2e8f0", textAlign: "center" }}>
          <p style={{ fontSize: 12, color: "#a0aec0", margin: 0 }}>
            © 2026 Orbis.tax · Versão 1.0 — Abril 2026
          </p>
          <p style={{ fontSize: 11, color: "#cbd5e0", marginTop: 4 }}>
            Dúvidas:{" "}
            <a href="mailto:contato@orbis.tax" style={{ color: "#3B9EE8" }}>contato@orbis.tax</a>
            {" · "}
            <Link href="/politica-privacidade" style={{ color: "#3B9EE8" }}>
              Política de Privacidade
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}

const h3Style: React.CSSProperties = {
  fontSize: 14,
  fontWeight: 700,
  color: "#1a2f4e",
  margin: "20px 0 8px",
  textTransform: "uppercase",
  letterSpacing: "0.3px",
};

function Section({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <div style={{
      background: "#fff",
      borderRadius: 8,
      padding: "28px 32px",
      boxShadow: "0 1px 4px rgba(0,0,0,.07)",
    }}>
      <h2 style={{
        fontSize: 16,
        fontWeight: 700,
        color: "#1a2f4e",
        margin: "0 0 16px",
        paddingBottom: 12,
        borderBottom: "2px solid #eff6ff",
      }}>
        {titulo}
      </h2>
      <div style={{ fontSize: 14, color: "#4a5568", lineHeight: 1.75 }}>
        {children}
      </div>
    </div>
  );
}

function Callout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      background: "#fffbeb",
      border: "1px solid #fcd34d",
      borderRadius: 6,
      padding: "12px 16px",
      fontSize: 13,
      color: "#92400e",
      lineHeight: 1.6,
      marginTop: 16,
    }}>
      {children}
    </div>
  );
}
