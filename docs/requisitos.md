# 🧩 ESCALA360 – Documento de Requisitos do Sistema  
**Versão:** 2.0  
**Autor:** Anderson de Matos Guimarães  
**Data:** 31/10/2025  

---

## 1. Visão Geral do Sistema

### 1.1 Contexto  
O **ESCALA360** é um sistema web desenvolvido como solução prática para o **desafio de Analista de Sistemas Pleno (Prova Prática)**, destinado à **gestão de escalas e plantões hospitalares**.  
O sistema centraliza o controle de **profissionais, turnos, substituições e auditoria de ações**, integrando a geração de relatórios e painéis de produtividade com **Plotly**.

O projeto é baseado no banco de dados oficial **`escala360.sql`**, fornecido pelo professor, e estruturado em **Flask + SQLAlchemy**, com modularização via **Blueprints** e interface responsiva (TailwindCSS).

---

## 2. Propósito e Objetivos

### 2.1 Propósito  
Automatizar o controle de plantões e substituições, eliminando processos manuais e melhorando a rastreabilidade das ações administrativas.

### 2.2 Objetivos Estratégicos  
- Reduzir conflitos de horário e sobreposição de plantões.  
- Facilitar a gestão e substituição de profissionais em regime de plantão.  
- Prover indicadores de desempenho e ocupação (painel BI).  
- Registrar todas as ações relevantes para auditoria.  
- Fornecer uma base técnica escalável e reutilizável para outros órgãos públicos.

---

## 3. Escopo do Sistema

| Módulo | Descrição | Entregável |
|--------|------------|------------|
| **Profissionais** | Cadastro e manutenção de médicos, enfermeiros e técnicos. | CRUD de profissionais. |
| **Plantões** | Definição de horários e locais de trabalho. | CRUD de turnos. |
| **Escalas** | Associação entre plantões e profissionais. | Interface de gestão de escalas. |
| **Substituições** | Registro e aprovação de trocas de plantão. | Formulário e controle de substituições. |
| **Auditoria** | Registro de logs de ações e eventos. | Listagem e exportação. |
| **Painel BI** | Indicadores de produtividade e ocupação. | Visualizações interativas (Plotly). |

---

## 4. Requisitos Funcionais (RF)

| Código | Descrição | Prioridade |
|---------|------------|-------------|
| RF01 | Cadastrar, editar e desativar profissionais. | Alta |
| RF02 | Cadastrar e editar turnos de plantão. | Alta |
| RF03 | Gerar escalas e vincular profissionais a turnos. | Alta |
| RF04 | Solicitar e aprovar substituições. | Alta |
| RF05 | Registrar logs automáticos em tabela de auditoria. | Alta |
| RF06 | Exibir indicadores e gráficos de produtividade. | Média |
| RF07 | Exportar relatórios e dados (CSV/PDF). | Média |
| RF08 | Notificar usuários por e-mail ou WhatsApp (futuro). | Baixa |
| RF09 | Registrar erros e falhas em log de sistema. | Alta |

---

## 5. Requisitos Não Funcionais (RNF)

| Código | Descrição | Categoria |
|---------|------------|-----------|
| RNF01 | O sistema deve ser responsivo (desktop e mobile). | Usabilidade |
| RNF02 | Deve utilizar Flask + SQLAlchemy. | Arquitetura |
| RNF03 | Deve manter logs persistentes em `logs/escala360.log`. | Auditoria |
| RNF04 | O tempo médio de resposta deve ser inferior a 3 segundos. | Desempenho |
| RNF05 | O banco de dados deve ser compatível com SQLite, MySQL e PostgreSQL. | Persistência |
| RNF06 | Toda exceção deve ser tratada por templates `404.html` e `500.html`. | Confiabilidade |
| RNF07 | Deve suportar execução local e deploy WSGI (Vercel). | Portabilidade |
| RNF08 | Deve permitir fácil configuração via `.env`. | Manutenibilidade |

---

## 6. Regras de Negócio (RN)

| Código | Regra | Descrição |
|---------|--------|-----------|
| RN01 | Plantão único | Um mesmo turno não pode ter mais de um profissional ativo. |
| RN02 | Carga horária máxima | Nenhum profissional pode ultrapassar 40h semanais. |
| RN03 | Substituição formal | Toda substituição deve ser solicitada e aprovada. |
| RN04 | Auditoria obrigatória | Todas as ações críticas são registradas. |
| RN05 | Substituições urgentes | Podem ser feitas com menos de 12h de antecedência, mediante justificativa. |
| RN06 | Plantão vago | O sistema deve sinalizar turnos sem profissional designado. |
| RN07 | Status de substituição | Pode ser “pendente”, “aprovada” ou “recusada”. |

---

## 7. Modelo de Dados (Conforme `escala360.sql`)

### 7.1 Tabelas Principais
| Tabela | Campos | Descrição |
|---------|---------|-----------|
| `profissionais` | `id`, `nome`, `cargo`, `email`, `telefone`, `ativo` | Cadastro de profissionais. |
| `plantoes` | `id`, `data`, `hora_inicio`, `hora_fim` | Horários e datas de plantão. |
| `escalas` | `id`, `id_profissional`, `id_plantao`, `status` | Relação profissional–plantão. |
| `substituicoes` | `id`, `id_escala`, `id_substituto`, `motivo`, `status` | Controle de trocas. |
| `auditoria` | `id`, `acao`, `tabela`, `registro_id`, `usuario`, `data_hora` | Log de ações no sistema. |

---

## 8. Consultas SQL Principais

### 8.1 Plantões vagos
```sql
SELECT * FROM plantoes
WHERE id NOT IN (SELECT id_plantao FROM escalas);
```

### 8.2 Substituições pendentes
```sql
SELECT s.id, p.nome AS profissional, s.motivo, s.status
FROM substituicoes s
JOIN escalas e ON e.id = s.id_escala
JOIN profissionais p ON p.id = e.id_profissional
WHERE s.status = 'pendente';
```

### 8.3 Carga horária por profissional
```sql
SELECT p.nome, COUNT(e.id) AS total_plantões
FROM profissionais p
JOIN escalas e ON e.id_profissional = p.id
GROUP BY p.nome;
```

---

## 9. Arquitetura Técnica

| Camada | Descrição |
|---------|------------|
| **Backend (Flask)** | Estrutura modular com Blueprints (`escalas`, `profissionais`, `plantoes`, `substituicoes`, `auditoria`). |
| **Banco (SQLAlchemy)** | ORM mapeando o modelo `models.py` e inicializado via `init_db.py`. |
| **Frontend (Jinja + Tailwind)** | Templates responsivos com dark mode. |
| **BI (Plotly)** | Painel interativo de produtividade. |
| **Logs** | Configurados em `config.py` e registrados em `logs/escala360.log`. |

---

## 10. Fluxo de Substituição

1. Profissional solicita substituição →  
2. Sistema verifica disponibilidade →  
3. Sugere até 3 substitutos →  
4. Supervisor aprova ou recusa →  
5. Auditoria registra a decisão.

---

## 11. Critérios de Aceitação

- O sistema deve inicializar corretamente o banco via `init_db.py`.  
- Todos os módulos devem carregar sem erro no `app.py`.  
- O painel BI deve exibir os indicadores de produtividade.  
- As páginas `404.html` e `500.html` devem estar funcionais.  
- Todas as operações CRUD devem ser persistidas no banco e registradas em log.

---

## 12. Métricas de Sucesso

| Métrica | Indicador | Meta |
|----------|------------|------|
| Redução de conflitos de plantão | ≥ 95% | Implantação bem-sucedida |
| Tempo médio de substituição | ≤ 5 minutos | Eficiência operacional |
| Tempo médio de resposta HTTP | ≤ 3 segundos | Desempenho satisfatório |
| Taxa de logs válidos | 100% | Confiabilidade do sistema |

---

## 13. Versão do Documento

| Versão | Data | Autor | Descrição |
|---------|------|--------|------------|
| 1.0 | 24/10/2025 | Anderson de Matos Guimarães | Versão inicial (pré-prova). |
| 2.0 | 31/10/2025 | Anderson de Matos Guimarães | Atualização com base na Prova Prática e banco oficial `escala360.sql`. |

---
