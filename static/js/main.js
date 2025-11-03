// =========================================================
// ESCALA360 - JavaScript Global
// Autor: Anderson de Matos Guimarães
// Data: 02/11/2025
// =========================================================
// Descrição:
// Controla as interações da interface, carregamento de dados
// via API Flask, atualização dos KPIs, exibição de gráficos
// Plotly e sistema de notificações (toasts).
// =========================================================

// ---------- 🔹 Endpoints ----------
const API = {
  status: "/api/status",
  kpis: "/api/kpis",
  auditoria: "/auditoria/api",
  profissionais: "/profissionais/api",
  substituicoes: "/substituicoes/api",
};

// ---------- 🔹 Utilitários ----------
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Erro ao buscar ${url}: ${res.status}`);
  return await res.json();
}

function showToast(msg, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <i class="fas ${
      type === "success"
        ? "fa-check-circle"
        : type === "error"
        ? "fa-times-circle"
        : "fa-info-circle"
    }"></i>
    <span>${msg}</span>
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// ---------- 📊 Painel BI ----------
async function carregarPainelBI() {
  try {
    const kpis = await fetchJSON(API.kpis);

    document.getElementById("kpi-profissionais").textContent =
      kpis.profissionais_ativos ?? "-";
    document.getElementById("kpi-plantoes").textContent =
      kpis.plantoes ?? "-";
    document.getElementById("kpi-substituicoes").textContent =
      kpis.substituicoes ?? "-";
    document.getElementById("kpi-produtividade").textContent =
      kpis.produtividade ?? "-";

    if (document.getElementById("grafico-prod")) {
      const trace = {
        x: kpis.semanas,
        y: kpis.produtividade_semanal,
        type: "scatter",
        mode: "lines+markers",
        marker: { color: "#4f46e5", size: 8 },
        line: { width: 3 },
      };

      const layout = {
        title: "Produtividade Semanal",
        xaxis: { title: "Semana" },
        yaxis: { title: "Produtividade (%)", range: [0, 100] },
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        font: { color: "var(--text)" },
      };

      Plotly.newPlot("grafico-prod", [trace], layout, { responsive: true });
    }
  } catch (err) {
    console.error(err);
    showToast("Falha ao carregar painel de produtividade.", "error");
  }
}

// ---------- 🔎 Listagem genérica ----------
async function listar(endpoint, tabelaId, campos) {
  try {
    const data = await fetchJSON(endpoint);
    const tbody = document.getElementById(tabelaId);
    if (!tbody) return;

    tbody.innerHTML = "";

    if (!data.length) {
      tbody.innerHTML = <tr><td colspan="${campos.length}" class="text-center text-gray-500 py-3">Nenhum registro encontrado.</td></tr>;
      return;
    }

    for (const item of data) {
      const tr = document.createElement("tr");
      campos.forEach((campo) => {
        const td = document.createElement("td");
        td.textContent = item[campo] ?? "-";
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    }
  } catch (e) {
    console.error(e);
    showToast("Erro ao listar registros.", "error");
  }
}

// ---------- 🔁 Inicialização ----------
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const status = await fetchJSON(API.status);
    console.log("✅ ESCALA360 Online:", status);
  } catch (e) {
    console.warn("⚠ API offline:", e.message);
  }
});
