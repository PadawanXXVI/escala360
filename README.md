# 🧭 Escala360 — Sistema de Gestão de Escalas e Painel BI Interativo

## 📄 Visão Geral

O **Escala360** é um sistema web desenvolvido em **Flask + Python + PostgreSQL**, projetado para **gerenciar escalas de profissionais, plantões e substituições**, oferecendo um **painel BI interativo** com métricas e visualizações em tempo real.

O sistema é modular, responsivo e documentado, atendendo padrões acadêmicos e profissionais.

---

## ⚙️ Tecnologias Principais

- **Python 3.11+**
- **Flask 3.x**
- **PostgreSQL 15+**
- **SQLAlchemy + Flask-Migrate**
- **Plotly.js (gráficos dinâmicos)**
- **Bootstrap 5 (design responsivo)**
- **dotenv (gerenciamento de variáveis de ambiente)**

---

## 🧱 Estrutura do Projeto

```
escala360/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   └── static/
├── docs/
│   ├── requisitos.md
│   ├── casos_de_uso.md
│   ├── logica_substitutos.md
│   ├── contrato_rest.md
│   ├── bpmn_alocacao_substituicao.drawio
│   └── apresentacao.pptx
├── escala360.sql
├── iniciar_database.py
├── app.py
├── .env.example
├── requirements.txt
└── .gitignore
```

---

## 🚀 Como Executar Localmente

### 1️⃣ Instalar dependências
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Configurar o ambiente
Crie um arquivo `.env` com base em `.env.example` e ajuste suas credenciais PostgreSQL.

> ⚠️ Se outro app Flask estiver usando a porta 5000, altere `FLASK_RUN_PORT=5050` no `.env`.

### 3️⃣ Criar o banco de dados
```bash
python iniciar_database.py
```

### 4️⃣ Executar o app
```bash
flask run
```
ou
```bash
python app.py
```

Acesse: [http://127.0.0.1:5050](http://127.0.0.1:5050)

---

## 📊 Painel BI Interativo

O sistema exibe gráficos dinâmicos com **Plotly.js**:
- 📈 Carga de plantões por profissional  
- 🧮 Status das substituições (pizza)  
- 📅 Plantões por dia (linha)

---

## 🧠 Lógica de Substitutos

Critérios automáticos:
- Mesmo cargo/função  
- Disponibilidade no horário  
- Menor carga ativa  
- Status ativo

Detalhes: `docs/logica_substitutos.md`

---

## 🧭 BPMN do Processo

Fluxo horizontal completo:
```
Profissional → Sistema Escala360 → Supervisor → Auditoria
```
Arquivo: `docs/bpmn_alocacao_substituicao.drawio`

---

## 🌐 API REST

Endpoints disponíveis:
- `GET /api/substituicoes` → lista substituições  
- `POST /api/substituicoes` → cria substituição  
- `POST /api/notificacoes/email` → simula envio de e-mail  
- `POST /api/notificacoes/whatsapp` → simula envio de WhatsApp

Documentação: `docs/contrato_rest.md`

---

## 📚 Documentação Técnica

- **Requisitos:** `docs/requisitos.md`  
- **Casos de Uso:** `docs/casos_de_uso.md`  
- **Apresentação:** `docs/apresentacao.pptx`

---

## 🧾 Licença
Este projeto foi desenvolvido para fins acadêmicos e de demonstração técnica.  
Todos os direitos reservados © 2025 — *Anderson de Matos Guimarães*.

---
