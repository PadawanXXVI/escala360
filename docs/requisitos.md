# ESCALA360 – Documento de Requisitos do Sistema  
**Versão:** 1.0  
**Autor:** Anderson de Matos Guimarães  
**Data:** 24/10/2025  

---

## 1. Visão Geral do Sistema

### 1.1 Contexto
O **ESCALA360** é um sistema web desenvolvido para automatizar a **gestão de ponto, escalas e produtividade** em órgãos públicos que operam sob regime de plantão, com foco inicial no **Tribunal de Justiça de São Paulo (TJSP)**.  
O sistema substitui planilhas manuais e fluxos descentralizados por uma plataforma única e inteligente, que integra **gestão operacional** e **análise de desempenho (BI)**.

### 1.2 Propósito
Garantir **eficiência, transparência e equidade** na alocação de servidores em escalas e plantões, automatizando processos de substituição, controle de carga horária e comunicação entre equipes.

### 1.3 Objetivos Estratégicos
- Automatizar a criação e o gerenciamento de escalas semanais/mensais;  
- Eliminar conflitos e sobrecargas de trabalho por meio de regras inteligentes;  
- Reduzir tempo de substituição de servidores ausentes;  
- Integrar notificações automáticas via e-mail e WhatsApp;  
- Consolidar relatórios e indicadores de produtividade;  
- Promover rastreabilidade e conformidade institucional.

### 1.4 Público-Alvo
- Gestores de unidade (chefes de cartório, coordenadores);  
- Servidores e escreventes do TJSP;  
- Setores de Recursos Humanos;  
- Auditoria e Controle Interno.

---

## 2. Escopo do Sistema

### 2.1 Entregas Principais
| Módulo | Entregável | Benefício |
|---------|-------------|-----------|
| Escalas e Plantões | Cadastro, visualização e edição de escalas | Reduz erros e melhora a previsibilidade operacional |
| Substituições | Algoritmo de sugestão automática de substitutos | Agilidade e equilíbrio de carga horária |
| Controle de Ponto | Registro e auditoria de batidas | Transparência e conformidade |
| Painel BI | Gráficos interativos (Plotly) com KPIs | Tomada de decisão baseada em dados |
| Notificações | Envio de alertas via e-mail/WhatsApp | Comunicação rápida e rastreável |
| Auditoria | Logs de alterações e aprovações | Segurança e rastreabilidade administrativa |

---

## 3. Requisitos Funcionais

| Código | Descrição | Prioridade |
|---------|------------|-------------|
| RF01 | Permitir o cadastro e edição de profissionais, unidades e funções. | Alta |
| RF02 | Permitir a criação e gerenciamento de escalas de trabalho. | Alta |
| RF03 | Registrar plantões e associar profissionais titulares. | Alta |
| RF04 | Permitir a solicitação e aprovação de substituições. | Alta |
| RF05 | Sugerir automaticamente substitutos compatíveis. | Alta |
| RF06 | Exibir indicadores de produtividade (BI) com gráficos interativos. | Alta |
| RF07 | Registrar e auditar as batidas de ponto. | Média |
| RF08 | Enviar notificações automáticas via e-mail/WhatsApp. | Média |
| RF09 | Gerar relatórios e exportar dados (CSV/PDF). | Média |
| RF10 | Registrar logs de auditoria de todas as operações. | Alta |

---

## 4. Requisitos Não Funcionais

| Código | Descrição | Categoria |
|---------|------------|-----------|
| RNF01 | O sistema deve ser acessível via navegador web responsivo. | Usabilidade |
| RNF02 | Deve possuir autenticação e controle de perfis (Gestor, Servidor, RH, Auditoria). | Segurança |
| RNF03 | Deve garantir rastreabilidade e conformidade com a LGPD. | Governança |
| RNF04 | Deve suportar ao menos 100 usuários simultâneos. | Desempenho |
| RNF05 | Deve utilizar banco de dados relacional (MySQL). | Persistência |
| RNF06 | Deve registrar logs de auditoria em arquivo e banco. | Auditoria |
| RNF07 | Deve apresentar dashboards interativos (Plotly). | Visualização |
| RNF08 | Código modular (Python + Flask), com arquitetura RESTful. | Arquitetura |
| RNF09 | Integração externa via APIs (e-mail e WhatsApp). | Integração |
| RNF10 | O tempo médio de resposta deve ser inferior a 3 segundos. | Desempenho |

---

## 5. Regras de Negócio (RN)

| Código | Regra | Descrição |
|---------|--------|-----------|
| RN01 | Carga Máxima Semanal | Nenhum profissional pode ultrapassar a carga máxima definida (ex: 40h/semana). |
| RN02 | Descanso Mínimo | Deve haver um intervalo mínimo de 11 horas entre o fim de um plantão e o início de outro. |
| RN03 | Conflito de Horário | O sistema deve impedir a alocação de dois plantões sobrepostos. |
| RN04 | Substituição | Toda substituição deve ser solicitada, aceita e aprovada antes da efetivação. |
| RN05 | Plantão Vago | Se um plantão estiver sem titular, o sistema deve gerar sugestões automáticas de substitutos. |
| RN06 | Notificações | Toda substituição ou alteração deve gerar notificação para os envolvidos. |
| RN07 | Auditoria | Todas as ações críticas (alocação, substituição, ponto) devem ser registradas com usuário, data e hora. |
| RN08 | BI Analítico | Indicadores devem ser atualizados em tempo real ou sob demanda pelo gestor. |

---

## 6. Casos de Uso

| Código | Nome | Atores | Descrição Resumida |
|---------|------|--------|--------------------|
| UC01 | Gerenciar Escalas | Gestor | Criação, edição e exclusão de escalas. |
| UC02 | Alocar Profissional | Gestor | Associa profissional a um plantão específico. |
| UC03 | Solicitar Substituição | Servidor | Solicita substituição informando motivo. |
| UC04 | Sugerir Substitutos | Sistema | Gera lista de candidatos elegíveis conforme regras. |
| UC05 | Aprovar Substituição | Gestor | Analisa e confirma substituições propostas. |
| UC06 | Registrar Ponto | Servidor | Registra batidas de ponto ou justificativas. |
| UC07 | Visualizar Painel BI | Gestor, RH | Exibe métricas e gráficos interativos. |
| UC08 | Enviar Notificações | Sistema | Envia alertas automáticos aos usuários. |
| UC09 | Gerar Relatórios | Gestor, Auditoria | Gera relatórios operacionais e de auditoria. |

---

## 7. Modelo de Dados Conceitual (Simplificado)

### 7.1 Entidades Principais
- **Profissional** (`id`, `nome`, `funcao`, `unidade_id`, `carga_max_semanal_h`, `email`, `whatsapp`)
- **Unidade** (`id`, `nome`, `sigla`)
- **Escala** (`id`, `unidade_id`, `nome`, `dt_inicio`, `dt_fim`)
- **Plantao** (`id`, `escala_id`, `inicio`, `fim`, `funcao`, `status`)
- **Alocacao** (`id`, `plantao_id`, `profissional_id`, `tipo`, `status`)
- **PedidoSubstituicao** (`id`, `plantao_id`, `solicitante_id`, `motivo`, `status`)
- **BatidaPonto** (`id`, `profissional_id`, `ts`, `tipo`, `origem`)
- **Notificacao** (`id`, `canal`, `destino`, `assunto`, `corpo`, `status`, `referencia_tipo`, `referencia_id`)

### 7.2 Relacionamentos
- Uma **Unidade** possui várias **Escalas**.  
- Uma **Escala** possui vários **Plantões**.  
- Um **Plantão** pode ter um ou mais **Profissionais** alocados.  
- Um **Profissional** pode registrar várias **Batidas de ponto**.  
- Um **Pedido de Substituição** pertence a um **Plantão** e é feito por um **Profissional**.  
- Cada **Notificação** referencia um **Plantão** ou **Substituição**.

---

## 8. Requisitos Técnicos e Tecnológicos

| Componente | Tecnologia | Função |
|-------------|-------------|--------|
| Linguagem | **Python 3.13+** | Backend e lógica de negócio |
| Framework Web | **Flask** | Estruturação de rotas e views |
| Banco de Dados | **MySQL / SQLite (dev)** | Armazenamento relacional |
| ORM | **SQLAlchemy** | Mapeamento objeto-relacional |
| Visualização | **Plotly** | Gráficos e dashboards interativos |
| Front-End | **Tailwind CSS / DaisyUI** | Interface responsiva e moderna |
| API REST | **Flask Blueprint + JSON** | Integração com e-mail/WhatsApp |
| Deploy | **Vercel / Render / Railway** | Hospedagem e execução |
| Versionamento | **Git + GitHub** | Controle de versão e CI/CD |
| Documentação | **Markdown (GitHub Docs)** | Padrão de entrega e rastreabilidade |

---

## 9. Critérios de Aceitação

- Todas as regras de negócio (RN01–RN08) devem ser validadas e aplicadas no backend.  
- O sistema deve impedir manualmente qualquer alocação que viole descanso mínimo ou carga máxima.  
- O painel BI deve refletir dados reais do banco ou dataset de simulação.  
- Notificações devem ser registradas em log (mesmo que mockadas).  
- O layout deve ser responsivo e acessível.  
- A documentação deve estar publicada em `/docs` no GitHub e renderizável em GitHub Pages.

---

## 10. Métricas de Sucesso

| Métrica | Indicador | Meta |
|----------|------------|------|
| Tempo médio de geração de escala | < 30 segundos | 90% das vezes |
| Taxa de substituição automatizada | ≥ 80% | Acurácia do algoritmo |
| Redução de conflitos de escala | ≥ 95% | Eliminação de sobreposição |
| Tempo médio de comunicação (e-mail/WhatsApp) | < 10 segundos | Notificação eficaz |
| Satisfação dos gestores | ≥ 9/10 | Avaliação interna |

---

## 11. Rastreabilidade

| Item | Origem | Local de Implementação |
|------|---------|------------------------|
| RN01, RN02, RN03 | Documento de requisitos | `services/sugestoes.py` |
| RN04–RN06 | BPMN / API | `routes/api.py` |
| RF01–RF10 | Casos de uso | `routes/web.py` |
| RNF01–RNF10 | Arquitetura | `app.py` e `models.py` |
| Consultas SQL | `docs/queries.md` | `repo/queries.sql` |

---

## 12. Versão do Documento

| Versão | Data | Autor | Alterações |
|---------|------|--------|-------------|
| 1.0 | 24/10/2025 | Anderson de Matos Guimarães | Criação inicial do documento de requisitos |

---
