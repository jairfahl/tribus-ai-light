import Link from "next/link";

export const metadata = {
  title: "SLA — Acordo de Nível de Serviço · Orbis.tax",
  description: "Acordo de Nível de Serviço (SLA) da plataforma Orbis.tax. Versão 1.0 — Abril 2026.",
};

export default function SlaPage() {
  return (
    <div style={{ background: "#f4f6f9", minHeight: "100vh", fontFamily: "'Segoe UI', Arial, sans-serif" }}>

      {/* Header */}
      <header style={{ background: "#1a2f4e", padding: "20px 40px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <Link href="/" style={{ textDecoration: "none" }}>
          <span style={{ fontSize: 20, fontWeight: 800, color: "#fff", letterSpacing: "-0.5px" }}>
            Orbis<span style={{ color: "#3B9EE8" }}>.tax</span>
          </span>
        </Link>
        <Link href="/login" style={{ fontSize: 13, color: "rgba(255,255,255,.70)", textDecoration: "none" }}>
          Entrar na plataforma →
        </Link>
      </header>

      {/* Conteúdo */}
      <main style={{ maxWidth: 860, margin: "0 auto", padding: "48px 24px 80px" }}>

        {/* Título */}
        <div style={{ marginBottom: 40 }}>
          <p style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, color: "#3B9EE8", marginBottom: 8 }}>
            Versão 1.0 — Abril 2026
          </p>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "#1a2f4e", margin: "0 0 12px" }}>
            SLA — Acordo de Nível de Serviço
          </h1>
          <p style={{ fontSize: 15, color: "#4a5568", lineHeight: 1.7, margin: 0 }}>
            Este documento define os níveis de serviço comprometidos pela <strong>Orbis.tax</strong> para
            os tenants contratantes, incluindo disponibilidade, suporte, manutenção e compensações
            aplicáveis em caso de descumprimento.
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>

          {/* Seção 2 */}
          <Section titulo="2. Disponibilidade">
            <h3 style={h3Style}>2.1 Uptime Comprometido por Plano</h3>
            <TableWrapper>
              <table style={tableStyle}>
                <thead>
                  <tr>
                    <Th>Métrica</Th>
                    <Th>Starter</Th>
                    <Th>Professional</Th>
                    <Th>Enterprise</Th>
                    <Th>Observação</Th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <Td bold>Uptime mensal</Td>
                    <Td>99,0%</Td>
                    <Td>99,5%</Td>
                    <Td>99,8%</Td>
                    <Td muted>Excluindo janelas de manutenção</Td>
                  </tr>
                  <tr style={{ background: "#f7fafc" }}>
                    <Td bold>Máx. indisponibilidade/mês</Td>
                    <Td>~7h12min</Td>
                    <Td>~3h39min</Td>
                    <Td>~1h27min</Td>
                    <Td muted>Tempo acumulado</Td>
                  </tr>
                  <tr>
                    <Td bold>Janela de manutenção</Td>
                    <Td>Sáb 02h–04h BRT</Td>
                    <Td>Sáb 02h–03h BRT</Td>
                    <Td>Acordada com tenant</Td>
                    <Td muted>Aviso prévio: 48h</Td>
                  </tr>
                </tbody>
              </table>
            </TableWrapper>

            <h3 style={h3Style}>2.2 Cálculo de Uptime</h3>
            <div style={{ background: "#f0f7ff", borderRadius: 6, padding: "12px 16px", fontFamily: "monospace", fontSize: 13, color: "#1a2f4e", margin: "8px 0 12px" }}>
              Uptime = (minutos totais do mês − minutos de indisponibilidade não programada) / minutos totais do mês × 100
            </div>
            <p>
              <strong>Não são computados como indisponibilidade:</strong> janelas de manutenção
              programadas, indisponibilidade de serviços terceiros (Anthropic API, Asaas) e
              incidentes decorrentes de ações do próprio tenant.
            </p>
          </Section>

          {/* Seção 3 */}
          <Section titulo="3. Suporte">
            <TableWrapper>
              <table style={tableStyle}>
                <thead>
                  <tr>
                    <Th>Item</Th>
                    <Th>Starter</Th>
                    <Th>Professional</Th>
                    <Th>Enterprise</Th>
                    <Th>Canal</Th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <Td bold>Horário de atendimento</Td>
                    <Td>Seg–Sex 9h–18h BRT</Td>
                    <Td>Seg–Sex 8h–20h BRT</Td>
                    <Td>24/7 para críticos</Td>
                    <Td muted>E-mail</Td>
                  </tr>
                  <tr style={{ background: "#f7fafc" }}>
                    <Td bold>SLA de 1ª resposta</Td>
                    <Td>2 dias úteis</Td>
                    <Td>8 horas úteis</Td>
                    <Td>4 horas</Td>
                    <Td muted>E-mail</Td>
                  </tr>
                  <tr>
                    <Td bold>Incidente crítico</Td>
                    <Td>4 horas</Td>
                    <Td>2 horas</Td>
                    <Td>1 hora</Td>
                    <Td muted>E-mail + WhatsApp</Td>
                  </tr>
                  <tr style={{ background: "#f7fafc" }}>
                    <Td bold>Canal de suporte</Td>
                    <Td>E-mail</Td>
                    <Td>E-mail + chat</Td>
                    <Td>E-mail + chat + WhatsApp</Td>
                    <Td muted>—</Td>
                  </tr>
                </tbody>
              </table>
            </TableWrapper>
            <p style={{ marginTop: 12 }}>
              E-mail de suporte:{" "}
              <a href="mailto:suporte@orbis.tax" style={{ color: "#2563eb" }}>suporte@orbis.tax</a>
            </p>
          </Section>

          {/* Seção 4 */}
          <Section titulo="4. Classificação de Incidentes">
            <TableWrapper>
              <table style={tableStyle}>
                <thead>
                  <tr>
                    <Th>Severidade</Th>
                    <Th>Definição</Th>
                    <Th>Exemplo</Th>
                    <Th>Meta de Resolução</Th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style={{ ...tdBase, fontWeight: 700, color: "#dc2626" }}>CRÍTICO</td>
                    <Td>Plataforma indisponível para todos os usuários do tenant</Td>
                    <Td>API fora, banco inacessível</Td>
                    <Td>4h (Starter) / 2h (Prof.) / 1h (Ent.)</Td>
                  </tr>
                  <tr style={{ background: "#f7fafc" }}>
                    <td style={{ ...tdBase, fontWeight: 700, color: "#d97706" }}>ALTO</td>
                    <Td>Funcionalidade principal comprometida para parte dos usuários</Td>
                    <Td>Análise RAG retornando erro</Td>
                    <Td>8h úteis</Td>
                  </tr>
                  <tr>
                    <td style={{ ...tdBase, fontWeight: 700, color: "#2563eb" }}>MÉDIO</td>
                    <Td>Funcionalidade secundária afetada, workaround disponível</Td>
                    <Td>Exportação de output lenta</Td>
                    <Td>2 dias úteis</Td>
                  </tr>
                  <tr style={{ background: "#f7fafc" }}>
                    <td style={{ ...tdBase, fontWeight: 700, color: "#6b7280" }}>BAIXO</td>
                    <Td>Questão estética ou melhoria sem impacto operacional</Td>
                    <Td>Ajuste visual na interface</Td>
                    <Td>Próximo ciclo de release</Td>
                  </tr>
                </tbody>
              </table>
            </TableWrapper>
          </Section>

          {/* Seção 5 */}
          <Section titulo="5. Compensações por Descumprimento">
            <p>Em caso de descumprimento do uptime comprometido, o tenant tem direito a crédito na próxima fatura:</p>
            <TableWrapper>
              <table style={tableStyle}>
                <thead>
                  <tr>
                    <Th>Uptime apurado no mês</Th>
                    <Th>Crédito (% da mensalidade)</Th>
                    <Th>Limite</Th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <Td>Abaixo do comprometido até 0,5%</Td>
                    <Td>10%</Td>
                    <Td>1 mensalidade</Td>
                  </tr>
                  <tr style={{ background: "#f7fafc" }}>
                    <Td>Abaixo do comprometido entre 0,5% e 1%</Td>
                    <Td>25%</Td>
                    <Td>1 mensalidade</Td>
                  </tr>
                  <tr>
                    <Td>Abaixo do comprometido acima de 1%</Td>
                    <Td>50%</Td>
                    <Td>1 mensalidade</Td>
                  </tr>
                </tbody>
              </table>
            </TableWrapper>
            <p style={{ marginTop: 12 }}>
              Compensações não se acumulam entre meses e devem ser solicitadas em até <strong>30 dias</strong> após
              o incidente. Não são aplicáveis durante o período de trial.
            </p>
          </Section>

          {/* Seção 6 */}
          <Section titulo="6. Exclusões de Responsabilidade">
            <p>O SLA não se aplica a indisponibilidades decorrentes de:</p>
            <ul>
              <li>Força maior ou caso fortuito</li>
              <li>Indisponibilidade de APIs de terceiros (Anthropic, Asaas, Voyage AI)</li>
              <li>Ações ou omissões do próprio tenant</li>
              <li>Ataques de negação de serviço (DDoS)</li>
              <li>Janelas de manutenção programadas e comunicadas</li>
            </ul>
          </Section>

          {/* Seção 7 */}
          <Section titulo="7. Monitoramento e Transparência">
            <p>
              A Orbis.tax mantém monitoramento contínuo de disponibilidade. Em caso de incidente crítico,
              o tenant será notificado por e-mail em até <strong>30 minutos</strong> após a detecção.
              Pós-incidente crítico: relatório de <em>post-mortem</em> disponibilizado em até{" "}
              <strong>5 dias úteis</strong>.
            </p>
          </Section>

          {/* Seção 8 */}
          <Section titulo="8. Revisão do SLA">
            <p>
              Este SLA é revisado anualmente ou sempre que houver alteração relevante na infraestrutura.
              Alterações que reduzam os níveis comprometidos serão comunicadas com{" "}
              <strong>60 dias de antecedência</strong>.
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
            <a href="mailto:suporte@orbis.tax" style={{ color: "#3B9EE8" }}>suporte@orbis.tax</a>
            {" · "}
            <Link href="/termos-de-uso" style={{ color: "#3B9EE8" }}>Termos de Uso</Link>
            {" · "}
            <Link href="/politica-privacidade" style={{ color: "#3B9EE8" }}>Política de Privacidade</Link>
          </p>
        </div>
      </main>
    </div>
  );
}

// ── Estilos compartilhados ──────────────────────────────────────────────────

const h3Style: React.CSSProperties = {
  fontSize: 14,
  fontWeight: 700,
  color: "#1a2f4e",
  margin: "20px 0 10px",
  textTransform: "uppercase",
  letterSpacing: "0.3px",
};

const tableStyle: React.CSSProperties = {
  width: "100%",
  borderCollapse: "collapse",
  fontSize: 13,
};

const tdBase: React.CSSProperties = {
  padding: "10px 14px",
  borderBottom: "1px solid #e2e8f0",
  verticalAlign: "top",
  color: "#4a5568",
};

// ── Componentes ─────────────────────────────────────────────────────────────

function Section({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <div style={{ background: "#fff", borderRadius: 8, padding: "28px 32px", boxShadow: "0 1px 4px rgba(0,0,0,.07)" }}>
      <h2 style={{ fontSize: 16, fontWeight: 700, color: "#1a2f4e", margin: "0 0 16px", paddingBottom: 12, borderBottom: "2px solid #eff6ff" }}>
        {titulo}
      </h2>
      <div style={{ fontSize: 14, color: "#4a5568", lineHeight: 1.75 }}>{children}</div>
    </div>
  );
}

function TableWrapper({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ overflowX: "auto", borderRadius: 6, border: "1px solid #e2e8f0", margin: "8px 0" }}>
      {children}
    </div>
  );
}

function Th({ children }: { children: React.ReactNode }) {
  return (
    <th style={{ padding: "10px 14px", background: "#1a2f4e", color: "#fff", textAlign: "left", fontSize: 12, fontWeight: 600, whiteSpace: "nowrap" }}>
      {children}
    </th>
  );
}

function Td({ children, bold, muted }: { children: React.ReactNode; bold?: boolean; muted?: boolean }) {
  return (
    <td style={{ ...tdBase, fontWeight: bold ? 600 : 400, color: muted ? "#94a3b8" : "#4a5568" }}>
      {children}
    </td>
  );
}
