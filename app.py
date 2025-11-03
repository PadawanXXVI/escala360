# ===========================================================
# 🚀 ESCALA360 — APLICAÇÃO FLASK PRINCIPAL
# ===========================================================
# Este arquivo inicializa a aplicação Flask, carregando
# a configuração definida em app/__init__.py e as variáveis
# do ambiente (.env).
# ===========================================================

from app import create_app

# Cria a aplicação Flask com todas as configurações,
# conexões, blueprints e extensões.
app = create_app()

# Ponto de entrada da aplicação.
if __name__ == "__main__":
    # Executa o servidor Flask no modo debug (configurado no .env)
    # Para produção, altere para app.run(debug=False, host="0.0.0.0")
    app.run(debug=True)
