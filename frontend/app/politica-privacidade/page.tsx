import Link from "next/link";

export const metadata = {
  title: "Política de Privacidade — Orbis.tax",
  description: "Política de Privacidade e Proteção de Dados Pessoais da Orbis.tax, em conformidade com a LGPD (Lei nº 13.709/2018).",
};

export default function PoliticaPrivacidadePage() {
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
            Versão 1.1 — Abril 2026
          </p>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "#1a2f4e", margin: "0 0 12px" }}>
            Política de Privacidade e Proteção de Dados Pessoais
          </h1>
          <p style={{ fontSize: 15, color: "#4a5568", lineHeight: 1.7, margin: 0 }}>
            A presente Política formaliza o compromisso institucional da <strong>Orbis.tax</strong> com a
            transparência, a segurança da informação e a proteção da privacidade de seus usuários,
            estabelecendo as normas que regem o tratamento de dados pessoais em estrita observância à
            Lei nº 13.709/2018 (LGPD), à Lei nº 12.965/2014 (Marco Civil da Internet) e ao Decreto
            nº 8.771/2016, entre as demais normas vigentes no Brasil.
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>

          {/* Seção 1 */}
          <Section titulo="1. Identificação do Controlador e do Encarregado (DPO)">
            <p>O tratamento de dados é realizado pela operadora da Orbis.tax, na qualidade de <strong>Controladora</strong> (Art. 5º, VI, LGPD).</p>
            <ul>
              <li><strong>Encarregado (DPO):</strong> Jair Fahl, designado nos termos do Art. 41 da LGPD.</li>
              <li><strong>Contato:</strong> <a href="mailto:dpo@orbis.tax" style={{ color: "#2563eb" }}>dpo@orbis.tax</a></li>
              <li><strong>Atribuições:</strong> atuar como canal de comunicação entre o controlador, os titulares e a ANPD; aceitar reclamações e orientar funcionários (Art. 41, § 2º, LGPD).</li>
            </ul>
          </Section>

          {/* Seção 2 */}
          <Section titulo="2. Princípios Norteadores e Dados Coletados">
            <p>Todas as operações de tratamento observam os princípios da boa-fé e os mandamentos do Art. 6º da LGPD, com destaque para:</p>
            <ul>
              <li><strong>Finalidade e Adequação:</strong> tratamento restrito a propósitos legítimos e informados (Art. 6º, I e II).</li>
              <li><strong>Necessidade:</strong> limitação ao mínimo necessário para a execução do serviço (Art. 6º, III).</li>
              <li><strong>Transparência:</strong> garantia de informações claras e precisas sobre os agentes de tratamento (Art. 6º, VI).</li>
            </ul>

            <h3 style={h3Style}>2.1 Dados de Cadastro do Tenant</h3>
            <ul>
              <li>Razão social e CNPJ raiz</li>
              <li>Nome, e-mail e função dos usuários cadastrados</li>
              <li>Dados de faturamento (processados pela Asaas — a Orbis.tax não armazena dados de cartão)</li>
            </ul>

            <h3 style={h3Style}>2.2 Dados de Uso da Plataforma</h3>
            <ul>
              <li>Cases criados: título, descrição, tributos, período de referência, áreas impactadas</li>
              <li>Premissas, hipóteses e decisões registradas no protocolo P1–P6</li>
              <li>Outputs gerados e aprovados</li>
              <li>Logs de acesso: IP, user agent, timestamp de login</li>
              <li>Dados de metering: registro de login mensal por usuário (MAU)</li>
            </ul>

            <h3 style={h3Style}>2.3 Dados Não Coletados</h3>
            <ul>
              <li>Dados de cartão de crédito ou conta bancária (processados exclusivamente pela Asaas)</li>
              <li>Dados pessoais sensíveis não relacionados à gestão tributária</li>
            </ul>
          </Section>

          {/* Seção 3 */}
          <Section titulo="3. Finalidades e Bases Legais para o Tratamento">
            <p>O tratamento fundamenta-se nas seguintes hipóteses do Art. 7º da LGPD:</p>
            <ul>
              <li><strong>Execução de Contrato (Art. 7º, V):</strong> para a prestação dos serviços de inteligência tributária e gestão de acesso.</li>
              <li><strong>Cumprimento de Obrigação Legal (Art. 7º, II):</strong> para guarda de logs e dados fiscais.</li>
              <li><strong>Legítimo Interesse (Art. 7º, IX):</strong> para segurança da plataforma e melhorias técnicas, respeitados os direitos e liberdades fundamentais.</li>
            </ul>
          </Section>

          {/* Seção 4 */}
          <Section titulo="4. Proibição de Comercialização de Dados">
            <p>A Orbis.tax reafirma seu compromisso com a ética e a privacidade:</p>
            <ul>
              <li><strong>Não Comercialização:</strong> é terminantemente proibida a venda, aluguel, cessão onerosa ou qualquer forma de comercialização de dados pessoais de usuários a terceiros para fins publicitários ou de monetização direta.</li>
              <li><strong>Finalidade e Transparência:</strong> o tratamento de dados ocorre exclusivamente para os propósitos legítimos informados nesta Política, vedado o tratamento posterior incompatível (Art. 6º, I e VI, LGPD).</li>
            </ul>
          </Section>

          {/* Seção 5 */}
          <Section titulo="5. Isolamento de Dados por Tenant e Compartilhamento com Suboperadores de IA">
            <p>Os dados de cada tenant são logicamente isolados no banco de dados. A Orbis.tax compartilha dados pessoais apenas com:</p>
            <ul>
              <li><strong>Asaas:</strong> dados necessários para processamento de pagamentos (nome, e-mail, CNPJ). Operador contratado com DPA vigente.</li>
              <li><strong>Anthropic (Claude API):</strong> conteúdo das consultas tributárias para processamento pelo modelo de linguagem. Não são enviados dados pessoais identificáveis desnecessariamente. Processamento sob regime de <em>zero retention</em>.</li>
              <li><strong>Voyage AI:</strong> textos para geração de embeddings. Processamento sem retenção de dados pelo fornecedor.</li>
              <li><strong>Autoridades públicas:</strong> quando exigido por lei ou ordem judicial.</li>
            </ul>
            <p>O uso de Anthropic (Claude) e Voyage AI observa o dever de transparência do Art. 9º, V da LGPD.</p>
          </Section>

          {/* Seção 6 */}
          <Section titulo="6. Retenção de Dados">
            <p>O término do tratamento ocorrerá quando a finalidade for alcançada ou por solicitação do titular (Art. 15, LGPD). Após o término, os dados serão eliminados, ressalvada a conservação para:</p>
            <ul>
              <li>Cumprimento de obrigação legal ou regulatória</li>
              <li>Uso exclusivo anonimizado (Art. 16, LGPD)</li>
            </ul>
          </Section>

          {/* Seção 7 */}
          <Section titulo="7. Direitos dos Titulares">
            <p>São assegurados aos titulares todos os direitos previstos no Art. 18 da LGPD, incluindo:</p>
            <ul>
              <li>Confirmação da existência de tratamento</li>
              <li>Acesso aos dados</li>
              <li>Correção de dados incompletos, inexatos ou desatualizados</li>
              <li>Anonimização, bloqueio ou eliminação de dados desnecessários</li>
              <li>Portabilidade dos dados</li>
              <li>Informação sobre compartilhamento</li>
              <li>Revogação do consentimento (quando aplicável)</li>
              <li>Revisão de decisões automatizadas (Art. 20, LGPD)</li>
            </ul>
            <p>
              <strong>Canal de contato:</strong> solicitações devem ser encaminhadas ao DPO pelo e-mail{" "}
              <a href="mailto:dpo@orbis.tax" style={{ color: "#2563eb" }}>dpo@orbis.tax</a>.{" "}
              <strong>Prazo de resposta:</strong> até 15 (quinze) dias corridos (Art. 19, II, LGPD).
            </p>
          </Section>

          {/* Seção 8 */}
          <Section titulo="8. Segurança da Informação e Gestão de Incidentes">
            <p>Adotamos medidas técnicas e administrativas aptas a proteger os dados (Art. 46, LGPD):</p>
            <ul>
              <li><strong>Dados em repouso:</strong> criptografados no banco PostgreSQL</li>
              <li><strong>Dados em trânsito:</strong> TLS 1.2+ obrigatório</li>
              <li><strong>Senhas:</strong> bcrypt com salt</li>
              <li><strong>Isolamento por tenant:</strong> isolamento lógico entre tenants no banco de dados</li>
              <li><strong>Acesso administrativo:</strong> restrito, auditado e com MFA</li>
            </ul>
            <p>Em caso de incidente de risco ou dano relevante, comunicaremos a ANPD e o titular conforme o Art. 48 da LGPD.</p>
          </Section>

          {/* Seção 9 — Responsabilidade */}
          <Section titulo="9. Responsabilidade e Sanções Administrativas">
            <p>A Orbis.tax compromete-se a manter a conformidade com a Lei nº 13.709/2018 (LGPD). O descumprimento das obrigações previstas nesta Política sujeita os agentes às sanções administrativas previstas no Art. 52 da LGPD.</p>
            <p>Sem prejuízo das sanções administrativas, a Orbis.tax, na qualidade de Controladora, responderá pelos danos patrimoniais, morais, individuais ou coletivos causados em razão do exercício de atividade de tratamento de dados pessoais que viole a legislação (Arts. 42 a 45, LGPD).</p>
            <p>A Orbis.tax não será responsabilizada quando demonstrar que: (I) não realizou o tratamento atribuído; (II) embora tenha realizado o tratamento, não houve violação à legislação; ou (III) o dano decorreu de culpa exclusiva do titular ou de terceiros.</p>
            <p><strong>Foro:</strong> Fica eleito o Foro da Comarca de Indaiatuba/SP para dirimir quaisquer controvérsias oriundas desta Política, com renúncia a qualquer outro, por mais privilegiado que seja.</p>
          </Section>

          {/* Seção 10 */}
          <Section titulo="10. Cookies e Registros de Acesso">
            <p>A plataforma Orbis.tax <strong>não utiliza cookies de rastreamento ou publicidade</strong>. Cookies de sessão são utilizados exclusivamente para manter o estado da sessão autenticada do usuário.</p>
            <p>Em cumprimento ao Art. 15 do Marco Civil da Internet, mantemos registros de acesso por 6 (seis) meses em ambiente controlado.</p>
          </Section>

          {/* Seção 11 */}
          <Section titulo="11. Alterações desta Política">
            <p>Esta Política poderá ser atualizada para refletir melhorias técnicas ou mudanças legislativas. Quaisquer alterações serão comunicadas com <strong>30 dias de antecedência</strong> por e-mail ao administrador do tenant e mediante aviso na plataforma.</p>
            <p>Caso ocorram alterações na finalidade ou forma do tratamento, o titular será informado com destaque e poderá revogar o consentimento se discordar das alterações (Art. 9º, § 2º e Art. 8º, § 6º, LGPD).</p>
          </Section>

          {/* Seção 12 */}
          <Section titulo="12. Contato e Disposições Finais">
            <ul>
              <li><strong>DPO:</strong> <a href="mailto:dpo@orbis.tax" style={{ color: "#2563eb" }}>dpo@orbis.tax</a></li>
              <li><strong>Suporte geral:</strong> <a href="mailto:contato@orbis.tax" style={{ color: "#2563eb" }}>contato@orbis.tax</a></li>
              <li><strong>ANPD:</strong> o titular pode peticionar perante a Autoridade Nacional de Proteção de Dados em <a href="https://www.gov.br/anpd" target="_blank" rel="noopener noreferrer" style={{ color: "#2563eb" }}>www.gov.br/anpd</a> (Art. 18, § 1º, LGPD).</li>
            </ul>
          </Section>

        </div>

        {/* Rodapé da página */}
        <div style={{ marginTop: 48, paddingTop: 24, borderTop: "1px solid #e2e8f0", textAlign: "center" }}>
          <p style={{ fontSize: 12, color: "#a0aec0", margin: 0 }}>
            © 2026 Orbis.tax · Versão 1.1 — Abril 2026
          </p>
          <p style={{ fontSize: 11, color: "#cbd5e0", marginTop: 4 }}>
            Sujeito a revisão jurídica. Para dúvidas:{" "}
            <a href="mailto:dpo@orbis.tax" style={{ color: "#3B9EE8" }}>dpo@orbis.tax</a>
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
