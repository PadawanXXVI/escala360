# ============================================================
# 🧩 Módulo de Rotas — Substituições
# ============================================================
# Este módulo é responsável por exibir a listagem das
# solicitações de substituição e suas situações atuais.
# ============================================================

from flask import Blueprint, render_template
from ..models import Substituicao

# Criação do Blueprint
bp = Blueprint("substituicoes", __name__, template_folder="../templates")


# ------------------------------------------------------------
# 🔹 Rota: /substituicoes
# ------------------------------------------------------------
@bp.route("/")
def listar():
    """Lista todas as solicitações de substituição, mais recentes primeiro."""
    substituicoes = Substituicao.query.order_by(Substituicao.data_solicitacao.desc()).all()
    return render_template("substituicoes.html", substituicoes=substituicoes)
