#!/bin/bash
# ============================================================
#  ESCALA360 - Setup Automático do Projeto (v4.1)
#  Compatível com GitHub CLI (sem jq e com milestones via API)
# ============================================================

OWNER="PadawanXXVI"
REPO="escala360"
PROJECT_NAME="escala360"

echo "🚀 Iniciando configuração automática do projeto ESCALA360..."

# ============================================================
# 0. Localizar o ID do projeto
# ============================================================
echo "🔍 Localizando ID do projeto '$PROJECT_NAME'..."

PROJECT_ID=$(gh project list --owner "$OWNER" --limit 20 2>/dev/null | grep -i "$PROJECT_NAME" | awk '{print $NF}')

if [ -z "$PROJECT_ID" ]; then
  echo "❌ ERRO: Projeto '$PROJECT_NAME' não encontrado."
  echo "ℹ️  Dica: verifique se o nome coincide exatamente com o título no GitHub Projects."
  exit 1
else
  echo "✅ Projeto localizado com ID: $PROJECT_ID"
fi

# ============================================================
# 1. Labels
# ============================================================
echo "🧩 Criando labels..."
gh label create "docs"       -R "$OWNER/$REPO" -d "Documentação do sistema"         --color BFD4F2 || true
gh label create "backend"    -R "$OWNER/$REPO" -d "Rotas Flask e lógica Python"     --color D4C5F9 || true
gh label create "frontend"   -R "$OWNER/$REPO" -d "Templates e UI (HTML, Tailwind)" --color FAE0C2 || true
gh label create "bi"         -R "$OWNER/$REPO" -d "Painel de BI e gráficos Plotly"  --color C2FAE0 || true
gh label create "deploy"     -R "$OWNER/$REPO" -d "Deploy e integração Vercel"      --color E0C2FA || true
gh label create "review"     -R "$OWNER/$REPO" -d "Revisão e testes"                --color FAE0E0 || true

# ============================================================
# 2. Milestones (via API)
# ============================================================
echo "📆 Criando milestones via API..."

create_milestone() {
  TITLE=$1
  DESC=$2
  DUE=$3
  echo "🪜 Criando milestone: $TITLE"
  gh api \
    --method POST \
    -H "Accept: application/vnd.github+json" \
    /repos/$OWNER/$REPO/milestones \
    -f title="$TITLE" \
    -f description="$DESC" \
    -f due_on="${DUE}T23:59:59Z" >/dev/null || true
}

create_milestone "Sprint 1 – Protótipo Web" "Telas Flask + protótipo visual funcionando localmente" "2025-10-24"
create_milestone "Sprint 2 – Deploy e Integrações" "Deploy no Vercel + API REST + BI finalizado" "2025-10-26"

# ============================================================
# 3. Função auxiliar para criar issues
# ============================================================
create_issue() {
  TITLE=$1
  BODY=$2
  LABEL=$3
  MILESTONE=$4
  echo "📝 Criando issue: $TITLE"
  gh issue create -R "$OWNER/$REPO" \
    --title "$TITLE" \
    --body "$BODY" \
    --label "$LABEL" \
    --milestone "$MILESTONE" >/dev/null || true
}

# ============================================================
# 4. Issues – conforme as etapas do projeto
# ============================================================
echo "🧱 Criando issues..."

# Etapa 1 – Documentação
create_issue "Criar docs/requisitos.md" "Documento de requisitos com regras e casos de uso." "docs" "Sprint 1 – Protótipo Web"
create_issue "Criar docs/casos_de_uso.md" "Definição dos casos de uso UC01–UC09." "docs" "Sprint 1 – Protótipo Web"
create_issue "Criar docs/bpmn.md" "Diagrama BPMN do processo de alocação/substituição." "docs" "Sprint 1 – Protótipo Web"
create_issue "Criar docs/queries.md" "Consultas SQL: carga máxima, plantões vagos, substituições pendentes." "docs" "Sprint 1 – Protótipo Web"
create_issue "Criar docs/sugestao_substitutos.md" "Lógica de sugestão de substitutos (pseudocódigo e fluxograma)." "docs" "Sprint 1 – Protótipo Web"
create_issue "Criar docs/api_contract.md" "Contrato REST para integração com e-mail e WhatsApp." "docs" "Sprint 1 – Protótipo Web"

# Etapa 2 – Desenvolvimento Flask
create_issue "Criar app.py com rotas básicas" "Definir rotas Flask: '/', '/escalas' e '/api/sugerir_substitutos'." "backend" "Sprint 1 – Protótipo Web"
create_issue "Criar templates/base.html" "Estrutura principal com Tailwind e Navbar." "frontend" "Sprint 1 – Protótipo Web"
create_issue "Criar templates/escalas.html" "Protótipo da tela de escalas com tabela e botão de substitutos." "frontend" "Sprint 1 – Protótipo Web"
create_issue "Criar templates/index.html (Painel BI)" "Painel de produtividade com KPIs e gráfico Plotly." "bi" "Sprint 1 – Protótipo Web"
create_issue "Testar execução local (flask run)" "Rodar o app localmente e validar rotas e templates." "backend" "Sprint 1 – Protótipo Web"

# Etapa 3 – BI e Visualização
create_issue "Integrar gráfico Plotly" "Adicionar gráfico de barras Plantões Alocados vs Vagos." "bi" "Sprint 2 – Deploy e Integrações"
create_issue "Criar indicadores de produtividade" "KPIs no painel (plantões vagos, alocados, substituições pendentes)." "bi" "Sprint 2 – Deploy e Integrações"
create_issue "Simular base de dados mock" "Criar dados estáticos para testes iniciais de visualização." "backend" "Sprint 2 – Deploy e Integrações"

# Etapa 4 – Integrações e Deploy
create_issue "Criar vercel.json" "Arquivo de configuração para deploy Flask no Vercel." "deploy" "Sprint 2 – Deploy e Integrações"
create_issue "Adicionar wsgi.py" "Arquivo de entrada WSGI para o Vercel." "deploy" "Sprint 2 – Deploy e Integrações"
create_issue "Deploy no Vercel" "Publicar o projeto em https://escala360.vercel.app" "deploy" "Sprint 2 – Deploy e Integrações"
create_issue "Atualizar README com link do projeto" "Adicionar instruções e link de acesso no README." "docs" "Sprint 2 – Deploy e Integrações"

# Etapa 5 – Apresentação
create_issue "Criar roteiro de 15 min (docs/apresentacao.md)" "Estruturar roteiro de apresentação do sistema ESCALA360." "docs" "Sprint 2 – Deploy e Integrações"
create_issue "Testar navegação final" "Executar navegação completa e validar fluxo do protótipo." "review" "Sprint 2 – Deploy e Integrações"

# ============================================================
# 5. Vincular todas as issues ao Project Escala360
# ============================================================
echo "🔗 Vinculando issues ao Project Escala360..."
for issue_number in $(gh issue list -R "$OWNER/$REPO" --json number --jq '.[].number'); do
  echo "➡️  Adicionando issue #$issue_number..."
  gh project item-add "$PROJECT_ID" --url "https://github.com/$OWNER/$REPO/issues/$issue_number" >/dev/null || true
done

echo "🎯 Projeto ESCALA360 configurado e vinculado com sucesso!"
