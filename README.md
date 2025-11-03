# 🧭 Escala360 — Sistema de Gestão de Escalas e Painel BI Interativo

## 📘 Visão Geral

O **Escala360** é um sistema web desenvolvido em **Flask + Python + PostgreSQL**, projetado para **gerenciar escalas, plantões e substituições** de profissionais, oferecendo um **Painel de BI interativo** totalmente integrado ao banco de dados.

O sistema é modular, responsivo e documentado, atendendo padrões acadêmicos e profissionais.  
Ele foi desenvolvido passo a passo, em 13 fases, com automação do banco de dados, lógica inteligente de substituição e visualização interativa de dados.

---

## ⚙️ Tecnologias Principais

- **Python 3.11+**
- **Flask 3.x**
- **PostgreSQL 15+**
- **SQLAlchemy + Flask-Migrate**
- **Plotly.js (gráficos dinâmicos)**
- **Bootstrap 5 (design responsivo)**
- **python-dotenv (configuração via .env)**

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

> ⚠️ Caso outro aplicativo Flask esteja rodando na porta 5000, altere `FLASK_RUN_PORT=5050` no `.env`.

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

📍 **Acesse:** [http://127.0.0.1:5050](http://127.0.0.1:5050)

---

## 📊 Painel BI Interativo

O sistema apresenta três gráficos dinâmicos com **Plotly.js**:
- 📈 **Barras:** Plantões por profissional  
- 🧮 **Pizza:** Status das substituições  
- 📅 **Linha:** Plantões por dia  

Essas visualizações são atualizadas automaticamente com base nas consultas SQL do banco de dados PostgreSQL.

---

## 🧠 Lógica de Sugestão de Substitutos

O Escala360 sugere automaticamente o melhor profissional substituto com base em critérios documentados:

- Mesmo cargo/função  
- Disponibilidade no horário  
- Menor carga de plantões ativos  
- Status ativo  

📄 Documentação completa em: `docs/logica_substitutos.md`

---

## 🧭 BPMN do Processo de Substituição

Fluxo horizontal completo do processo:

```
Profissional → Sistema Escala360 → Supervisor → Auditoria
```

📎 Arquivo: `docs/bpmn_alocacao_substituicao.drawio`  
Representa o processo de solicitação, sugestão e aprovação de substituições.

---

## 🌐 API REST

Endpoints REST documentados em `docs/contrato_rest.md`:

| Método | Rota | Descrição |
|---------|------|------------|
| `GET` | `/api/substituicoes` | Lista substituições pendentes ou todas |
| `POST` | `/api/substituicoes` | Cria nova solicitação |
| `POST` | `/api/notificacoes/email` | Simula envio de e-mail |
| `POST` | `/api/notificacoes/whatsapp` | Simula envio de notificação via WhatsApp |

Todos retornam respostas JSON padronizadas.

---

## 📚 Documentação Técnica

O diretório `/docs` contém todos os artefatos técnicos do projeto:

| Documento | Descrição |
|------------|------------|
| `requisitos.md` | Requisitos funcionais e não funcionais |
| `casos_de_uso.md` | Casos de uso UC01–UC06 |
| `logica_substitutos.md` | Lógica e pseudocódigo da sugestão automática |
| `contrato_rest.md` | Contrato da API REST |
| `bpmn_alocacao_substituicao.drawio` | Fluxo BPMN do processo de substituição |
| `apresentacao.pptx` | Apresentação acadêmica completa |

---

## ⚙️ Banco de Dados Automatizado

O script `iniciar_database.py`:
- Cria o banco `escala360` se não existir;  
- Executa o script SQL `escala360.sql`;  
- Verifica se as tabelas já existem (evitando sobrescrita);  
- Popula dados iniciais de forma segura.  

📈 Banco de dados utilizado: **PostgreSQL 15+**

---

## 🧾 Boas Práticas Implementadas

✅ Modularização com Blueprints  
✅ HTML5 semântico e acessível  
✅ Responsividade (Bootstrap 5)  
✅ ORM SQLAlchemy + Flask-Migrate  
✅ `.env` e `.env.example` (segurança e portabilidade)  
✅ Commits semânticos (`feat:`, `fix:`, `docs:` etc.)  
✅ Documentação técnica completa  
✅ Painel BI interativo e atualizado em tempo real  

---

## 🏷️ Release Final

A versão estável do projeto está publicada como **Release v1.0.0**.  
Ela marca a conclusão de todas as 13 fases do Escala360, incluindo código-fonte, documentação e apresentação.

📦 **Release:** [Versão Final — Escala360 v1.0.0](https://github.com/PadawanXXVI/escala360/releases/tag/v1.0.0)

> A release contém:  
> - Código completo e funcional  
> - Documentação técnica e BPMN  
> - Slides acadêmicos em `.pptx`  
> - `.env.example` para configuração local

---

## 🧠 Créditos e Licença

Desenvolvido por **Anderson de Matos Guimarães**  
📍 Projeto acadêmico — *Faculdade de Tecnologia e Inovação Senac-DF*  
📅 Novembro de 2025  

Licença: Livre para fins educacionais e demonstração técnica.  
© 2025 — *Todos os direitos reservados.*

---
