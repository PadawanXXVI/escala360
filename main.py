# ===========================================================
# 🚀 ESCALA360 — APLICAÇÃO FLASK PRINCIPAL
# ===========================================================
# Inicializa a aplicação Flask, carregando as configurações
# do módulo app/__init__.py e variáveis de ambiente (.env)
# ===========================================================

from app import create_app

# Cria a aplicação Flask com todas as configurações
app = create_app()

# Ponto de entrada local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
