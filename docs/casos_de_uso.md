# 🎯 Casos de Uso — Escala360

## 🧩 Visão Geral

Os **casos de uso** descrevem as principais interações entre os **atores** (usuários e sistema) e o **Escala360**, especificando o comportamento esperado do sistema sob diferentes condições.

Esses casos foram elaborados com base nos **requisitos funcionais (RF)** documentados no arquivo `docs/requisitos.md`.

---

## 👥 Atores Envolvidos

| Ator | Descrição |
|------|------------|
| **Profissional** | Usuário que atua em plantões e pode solicitar substituições. |
| **Supervisor** | Responsável pela análise e aprovação das substituições. |
| **Sistema Escala360** | Responsável por processar dados, gerar BI e sugerir substitutos. |
| **Administrador** | Responsável pelo gerenciamento de cadastros e configurações gerais. |

---

## 🧾 Lista de Casos de Uso

| Código | Nome | Atores principais |
|---------|------|-------------------|
| **UC01** | Gerenciar Profissionais | Administrador |
| **UC02** | Registrar e Gerenciar Plantões | Administrador |
| **UC03** | Solicitar Substituição | Profissional |
| **UC04** | Sugerir Substituto Automaticamente | Sistema Escala360 |
| **UC05** | Aprovar ou Recusar Substituição | Supervisor |
| **UC06** | Visualizar Painel BI | Todos os usuários |

---

## 🧮 UC01 — Gerenciar Profissionais

**Atores:** Administrador  
**Objetivo:** Cadastrar, editar e listar profissionais.  
**Pré-condição:** O administrador deve estar autenticado (versão futura).  
**Fluxo Principal:**
1. O administrador acessa o menu “Profissionais”.
2. O sistema exibe a lista de profissionais cadastrados.
3. O administrador insere ou atualiza informações.
4. O sistema valida e salva os dados no banco.

**Fluxo Alternativo:**
- 3a. Se algum campo obrigatório estiver vazio, o sistema exibe uma mensagem de erro.
- 3b. Se o e-mail já existir, o sistema solicita alteração.

---

## 🩺 UC02 — Registrar e Gerenciar Plantões

**Atores:** Administrador  
**Objetivo:** Cadastrar e consultar plantões disponíveis.  
**Pré-condição:** Devem existir profissionais e funções cadastrados.  
**Fluxo Principal:**
1. O administrador acessa “Plantões”.
2. O sistema exibe os plantões existentes.
3. O administrador cadastra um novo plantão (data, hora e local).
4. O sistema registra o plantão e o torna disponível na escala.

**Fluxo Alternativo:**
- 3a. Se o horário for inválido (hora início ≥ hora fim), o sistema exibe alerta.
- 3b. Se houver conflito de data/horário, o sistema bloqueia o cadastro.

---

## 🔁 UC03 — Solicitar Substituição

**Atores:** Profissional  
**Objetivo:** Solicitar substituição em um plantão previamente alocado.  
**Pré-condição:** O profissional deve estar alocado em um plantão ativo.  
**Fluxo Principal:**
1. O profissional acessa o menu “Substituições”.
2. Seleciona o plantão a ser substituído.
3. Informa o motivo e solicita a substituição.
4. O sistema registra a solicitação com status “pendente”.
5. O sistema executa automaticamente a lógica de sugestão (UC04).

**Fluxo Alternativo:**
- 3a. Se o profissional não tiver plantões ativos, o sistema exibe aviso.
- 3b. Se o mesmo plantão já tiver solicitação pendente, o sistema bloqueia nova solicitação.

---

## 🧠 UC04 — Sugerir Substituto Automaticamente

**Atores:** Sistema Escala360  
**Objetivo:** Encontrar o melhor substituto disponível para o plantão.  
**Pré-condição:** Deve existir uma solicitação pendente de substituição.  
**Fluxo Principal:**
1. O sistema identifica o cargo e horário do plantão.
2. Busca profissionais do mesmo cargo e com status “ativo”.
3. Verifica disponibilidade no horário.
4. Ordena os candidatos por carga de plantões.
5. Sugere o profissional com menor carga ativa.

**Fluxo Alternativo:**
- 3a. Se nenhum profissional estiver disponível, o sistema exibe mensagem “sem substituto disponível”.
- 5a. O supervisor poderá solicitar nova sugestão manualmente.

---

## 🧾 UC05 — Aprovar ou Recusar Substituição

**Atores:** Supervisor  
**Objetivo:** Avaliar a substituição sugerida pelo sistema e aprová-la ou recusá-la.  
**Pré-condição:** Deve existir substituição pendente.  
**Fluxo Principal:**
1. O supervisor acessa o menu “Substituições”.
2. O sistema exibe a lista de substituições pendentes.
3. O supervisor analisa a sugestão e escolhe “Aprovar” ou “Recusar”.
4. O sistema atualiza o status e registra o evento na tabela de auditoria.
5. O sistema envia notificações simuladas (e-mail e WhatsApp).

**Fluxo Alternativo:**
- 3a. Se o supervisor recusar, o sistema solicita nova sugestão (reinicia UC04).
- 4a. Se houver falha no envio de notificação, o sistema registra erro de comunicação.

---

## 📊 UC06 — Visualizar Painel BI

**Atores:** Todos os usuários (Administrador, Profissional, Supervisor)  
**Objetivo:** Consultar informações gerenciais e estatísticas do sistema.  
**Pré-condição:** O banco de dados deve conter registros de plantões e substituições.  
**Fluxo Principal:**
1. O usuário acessa a página inicial `/`.
2. O sistema executa as consultas SQL pré-definidas.
3. Os dados são enviados ao template `index.html`.
4. O painel BI exibe os gráficos de barras, pizza e linha com Plotly.js.

**Fluxo Alternativo:**
- 2a. Se não houver dados, o painel exibe “Sem dados disponíveis”.
- 3a. Se ocorrer erro de conexão ao banco, o sistema exibe alerta técnico.

---

## 🧾 Considerações Finais

Os casos de uso do **Escala360** foram definidos para garantir:
- **Rastreabilidade direta com os requisitos funcionais (RF)**;  
- **Clareza nos fluxos principais e alternativos**;  
- **Cobertura completa das funcionalidades essenciais** do sistema.  

Esses casos de uso também servirão de base para a **documentação dos testes de aceitação** e para futuras melhorias no sistema (ex.: autenticação e controle de acesso).

---

📅 **Versão:** 1.0  
👨‍💻 **Autor:** Anderson de Matos Guimarães  
🏛️ **Projeto:** Escala360 — Sistema de Gestão de Escalas e BI Interativo  
🕓 **Atualizado em:** Novembro de 2025
