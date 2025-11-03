# ============================================================
# 🧩 Módulo de Rotas — Plantões
# ============================================================
# Este módulo é responsável por exibir a listagem dos
# plantões cadastrados no sistema Escala360.
# ============================================================

from flask import Blueprint, render_template
from ..models import Plantao

# Criação do Blueprint
bp = Blueprint("plantoes", __name__, template_folder="../templates")


# ------------------------------------------------------------
# 🔹 Rota: /plantoes
# ------------------------------------------------------------
@bp.route("/")
def listar():
    """Lista todos os plantões cadastrados, ordenados por data e hora."""
    plantoes = Plantao.query.order_by(Plantao.data, Plantao.hora_inicio).all()
    return render_template("plantoes.html", plantoes=plantoes)
