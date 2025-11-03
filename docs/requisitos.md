# 📘 Requisitos do Sistema — Escala360

## 🧩 Visão Geral

O **Escala360** é um sistema web desenvolvido em **Flask + Python + PostgreSQL**, com o objetivo de **gerenciar escalas de profissionais, plantões e substituições**, além de oferecer um **Painel de BI interativo** para análise em tempo real.

O projeto integra conceitos de **engenharia de software**, **visualização de dados** e **automação de processos administrativos**, sendo totalmente modular, documentado e responsivo.

---

## ⚙️ Requisitos Funcionais (RF)

| Código | Requisito | Descrição |
|---------|------------|-----------|
| **RF01** | Cadastro de profissionais | O sistema deve permitir cadastrar, listar e visualizar profissionais ativos e inativos. |
| **RF02** | Cadastro de plantões | O sistema deve permitir registrar plantões com data, horário e função. |
| **RF03** | Alocação de profissionais em escalas | Cada plantão deve ser vinculado a um ou mais profissionais. |
| **RF04** | Solicitação de substituição | O profissional pode solicitar substituição, informando motivo e período. |
| **RF05** | Sugestão automática de substitutos | O sistema deve sugerir automaticamente o melhor substituto com base em critérios definidos (cargo, disponibilidade, carga e status). |
| **RF06** | Aprovação de substituições | O supervisor pode aprovar ou recusar uma substituição sugerida. |
| **RF07** | Painel BI interativo | A página inicial deve exibir gráficos dinâmicos de carga de plantões, status de substituições e plantões por dia. |
| **RF08** | Consultas SQL otimizadas | O sistema deve executar consultas SQL para alimentar o painel BI e relatórios internos. |
| **RF09** | Registro de auditoria | Toda substituição aprovada ou recusada deve ser registrada na tabela de auditoria. |
| **RF10** | Envio de notificações simuladas | O sistema deve simular notificações via e-mail e WhatsApp após cada decisão de substituição. |
| **RF11** | Exportação de dados | O sistema deve permitir exportar relatórios em formato CSV ou PDF (versão futura). |
| **RF12** | Autenticação básica (versão futura) | O sistema poderá ter login e controle de acesso. |

---

## ⚙️ Requisitos Não Funcionais (RNF)

| Código | Requisito | Descrição |
|---------|------------|-----------|
| **RNF01** | Arquitetura modular | O sistema deve utilizar o padrão MVC (Model-View-Controller) com Blueprints Flask. |
| **RNF02** | Banco de dados relacional | Deve utilizar PostgreSQL versão 15 ou superior. |
| **RNF03** | ORM | A persistência deve ser gerenciada via SQLAlchemy. |
| **RNF04** | Responsividade | O frontend deve ser compatível com dispositivos móveis, tablets e desktops. |
| **RNF05** | Acessibilidade | O HTML deve seguir boas práticas de acessibilidade (uso de `aria-label`, `role`, e contraste adequado). |
| **RNF06** | Compatibilidade | O sistema deve funcionar em navegadores modernos (Chrome, Edge, Firefox, Safari). |
| **RNF07** | Visualização de dados | Os gráficos devem ser interativos, utilizando Plotly.js. |
| **RNF08** | Segurança de credenciais | As variáveis sensíveis devem ser armazenadas no arquivo `.env`. |
| **RNF09** | Controle de versão | O código deve ser versionado via Git e hospedado no GitHub. |
| **RNF10** | Documentação completa | O sistema deve conter documentação técnica, de requisitos, casos de uso e BPMN. |
| **RNF11** | Padrões de commits | Todos os commits devem seguir convenções semânticas (`feat:`, `fix:`, `docs:` etc.). |
| **RNF12** | Escalabilidade | O sistema deve permitir fácil migração para banco remoto e ambiente em nuvem. |

---

## 💡 Requisitos de Interface (RI)

| Código | Requisito | Descrição |
|---------|------------|-----------|
| **RI01** | Layout base unificado | Todas as páginas devem herdar o template `base.html`. |
| **RI02** | Cores e tipografia padrão | O CSS deve utilizar tons azuis e neutros, com fonte Segoe UI/Roboto. |
| **RI03** | Estrutura semântica | O HTML deve utilizar tags `<header>`, `<main>`, `<section>`, `<article>`, `<footer>`. |
| **RI04** | Navegação simples | O menu superior deve conter links para as seções principais. |
| **RI05** | Indicadores visuais | Os status devem ser exibidos via `badge` colorido. |
| **RI06** | Feedback ao usuário | O sistema deve exibir mensagens amigáveis em caso de erro ou ausência de dados. |

---

## 🧭 Requisitos de Manutenção (RM)

| Código | Requisito | Descrição |
|---------|------------|-----------|
| **RM01** | Código documentado | Cada módulo Python deve conter comentários explicativos. |
| **RM02** | Facilidade de atualização | Novas funções devem ser integráveis sem reescrever módulos existentes. |
| **RM03** | Scripts automatizados | O sistema deve conter o script `iniciar_database.py` para configurar o banco automaticamente. |
| **RM04** | Estrutura clara de diretórios | Todos os módulos devem seguir a hierarquia padrão definida na Fase 1. |

---

## 🧾 Requisitos de Desempenho (RD)

| Código | Requisito | Descrição |
|---------|------------|-----------|
| **RD01** | Tempo de resposta | As consultas SQL e gráficos devem ser renderizados em até 2 segundos. |
| **RD02** | Capacidade de carga | O sistema deve suportar pelo menos 100 registros simultâneos sem degradação perceptível. |
| **RD03** | Otimização de consultas | As queries do painel BI devem usar `JOIN` e índices conforme necessário. |

---

## 🧠 Considerações Finais

O documento de requisitos do **Escala360** garante que o projeto siga **padrões de engenharia de software**, **boas práticas de desenvolvimento** e **requisitos de acessibilidade e desempenho** adequados a um sistema acadêmico-profissional.

Todos os requisitos aqui descritos foram **verificados e implementados até a Fase 10**, e servem como **base técnica e de avaliação** para o professor orientador.

---

📅 **Versão:** 1.0  
👨‍💻 **Autor:** Anderson de Matos Guimarães  
🏛️ **Projeto:** Escala360 — Sistema de Gestão de Escalas e BI Interativo  
🕓 **Atualizado em:** Novembro de 2025
