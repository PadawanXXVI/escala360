# ============================================================
# 🧩 Módulo de Rotas — Escalas
# ============================================================
# Este módulo é responsável por exibir a listagem geral das
# escalas cadastradas, com informações de plantões e profissionais.
# ============================================================

from flask import Blueprint, render_template
from ..models import Escala

# Criação do Blueprint
bp = Blueprint("escalas", __name__, template_folder="../templates")


# ------------------------------------------------------------
# 🔹 Rota: /escalas
# ------------------------------------------------------------
@bp.route("/")
def listar():
    """Lista todas as escalas, exibindo a data de alocação mais recente primeiro."""
    escalas = Escala.query.order_by(Escala.data_alocacao.desc()).all()
    return render_template("escalas.html", escalas=escalas)
