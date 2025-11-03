# ============================================================
# 🧩 Módulo de Rotas — Profissionais
# ============================================================
# Este módulo é responsável por exibir a listagem dos
# profissionais cadastrados no sistema Escala360.
# ============================================================

from flask import Blueprint, render_template
from ..models import Profissional

# Criação do Blueprint
bp = Blueprint("profissionais", __name__, template_folder="../templates")


# ------------------------------------------------------------
# 🔹 Rota: /profissionais
# ------------------------------------------------------------
@bp.route("/")
def listar():
    """Lista todos os profissionais cadastrados."""
    profissionais = Profissional.query.order_by(Profissional.nome).all()
    return render_template("profissionais.html", profissionais=profissionais)
