/* =========================================================
   ESCALA360 - Main JavaScript
   Interatividade e experiência do usuário (UX/UI)
   Autor: Anderson de Matos Guimarães
   Data: 31/10/2025
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  // ===============================================
  // 🌓 1. Modo Escuro Persistente
  // ===============================================
  const html = document.documentElement;
  const toggle = document.querySelector("#darkToggle");
  const storedTheme = localStorage.getItem("theme");

  if (storedTheme === "dark") html.classList.add("dark");
  if (storedTheme === "light") html.classList.remove("dark");

  if (toggle) {
    toggle.addEventListener("click", () => {
      html.classList.toggle("dark");
      const isDark = html.classList.contains("dark");
      localStorage.setItem("theme", isDark ? "dark" : "light");
      toast(isDark ? "🌙 Modo escuro ativado" : "☀️ Modo claro ativado");
    });
  }

  // ===============================================
  // 🔄 2. Transição suave entre páginas
  // ===============================================
  document.querySelectorAll("a[href]").forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#") || href.startsWith("javascript")) return;
      document.body.classList.add("fade-out");
      e.preventDefault();
      setTimeout(() => (window.location = href), 250);
    });
  });

  // ===============================================
  // 👥 3. CRUD - Profissionais
  // ===============================================
  if (window.location.pathname.includes("/profissionais")) {
    const form = document.querySelector("#form-profissional");
    const tbody = document.querySelector("#tabela-profissionais tbody");

    if (!form || !tbody) return;

    carregarProfissionais();

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        nome: form.nome.value,
        cargo: form.cargo.value,
        email: form.email.value,
        ativo: form.ativo.checked,
      };

      try {
        const res = await fetch("/profissionais/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }).then((r) => r.json());

        if (res.ok) {
          toast("✅ Profissional cadastrado!");
          form.reset();
          carregarProfissionais();
        } else throw new Error(res.error || "Erro desconhecido");
      } catch (err) {
        toast("❌ " + err.message);
      }
    });

    async function carregarProfissionais() {
      try {
        const data = await fetch("/profissionais/api").then((r) => r.json());
        renderProfissionais(data);
      } catch {
        toast("⚠️ Falha ao carregar profissionais.");
      }
    }

    function renderProfissionais(data) {
      if (!data.length) {
        tbody.innerHTML =
          '<tr><td colspan="4" class="text-center py-4 text-gray-400">Nenhum profissional cadastrado.</td></tr>';
        return;
      }

      tbody.innerHTML = data
        .map(
          (p) => `
          <tr>
            <td class="px-4 py-2">${p.nome}</td>
            <td class="px-4 py-2">${p.cargo || "—"}</td>
            <td class="px-4 py-2">${p.email}</td>
            <td class="px-4 py-2 ${
              p.ativo ? "text-green-600" : "text-red-600"
            }">${p.ativo ? "Ativo" : "Inativo"}</td>
          </tr>`
        )
        .join("");
    }
  }

  // ===============================================
  // 🕒 4. CRUD - Plantões
  // ===============================================
  if (window.location.pathname.includes("/plantoes")) {
    const form = document.querySelector("#form-plantao");
    const tbody = document.querySelector("#tabela-plantoes tbody");

    if (!form || !tbody) return;

    carregarPlantoes();

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        nome: form.nome.value,
        inicio: form.inicio.value,
        fim: form.fim.value,
      };

      try {
        const res = await fetch("/plantoes/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }).then((r) => r.json());

        if (res.ok) {
          toast("✅ Plantão cadastrado!");
          form.reset();
          carregarPlantoes();
        } else throw new Error(res.error || "Erro desconhecido");
      } catch (err) {
        toast("❌ " + err.message);
      }
    });

    async function carregarPlantoes() {
      try {
        const data = await fetch("/plantoes/api").then((r) => r.json());
        renderPlantoes(data);
      } catch {
        toast("⚠️ Falha ao carregar plantões.");
      }
    }

    function renderPlantoes(data) {
      if (!data.length) {
        tbody.innerHTML =
          '<tr><td colspan="3" class="text-center py-4 text-gray-400">Nenhum plantão cadastrado.</td></tr>';
        return;
      }

      tbody.innerHTML = data
        .map(
          (p) => `
          <tr>
            <td class="px-4 py-2">${p.nome}</td>
            <td class="px-4 py-2">${p.inicio} - ${p.fim}</td>
            <td class="px-4 py-2 text-right">
              <button class="btn-outline text-sm delete-btn" data-id="${p.id}">🗑️</button>
            </td>
          </tr>`
        )
        .join("");

      tbody.querySelectorAll(".delete-btn").forEach((btn) =>
        btn.addEventListener("click", () => excluirPlantao(btn.dataset.id))
      );
    }

    async function excluirPlantao(id) {
      if (!confirm("Deseja excluir este plantão?")) return;
      const res = await fetch(`/plantoes/api/${id}`, { method: "DELETE" }).then((r) => r.json());
      if (res.ok) {
        toast("🗑️ Plantão excluído!");
        carregarPlantoes();
      } else toast("❌ " + (res.error || "Erro ao excluir."));
    }
  }

  // ===============================================
  // 📋 5. CRUD - Escalas
  // ===============================================
  if (window.location.pathname.includes("/escalas")) {
    const form = document.querySelector("#form-escala");
    const tbody = document.querySelector("#tabela-escalas tbody");

    if (!form || !tbody) return;

    carregarEscalas();

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        funcionario_id: form.funcionario_id.value,
        turno_id: form.turno_id.value,
        data: form.data.value,
        status: form.status.value,
      };

      try {
        const res = await fetch("/escalas/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }).then((r) => r.json());

        if (res.ok) {
          toast("✅ Escala cadastrada!");
          form.reset();
          carregarEscalas();
        } else throw new Error(res.error || "Erro desconhecido");
      } catch (err) {
        toast("❌ " + err.message);
      }
    });

    async function carregarEscalas() {
      try {
        const data = await fetch("/escalas/api").then((r) => r.json());
        renderEscalas(data);
      } catch {
        toast("⚠️ Falha ao carregar escalas.");
      }
    }

    function renderEscalas(data) {
      if (!data.length) {
        tbody.innerHTML =
          '<tr><td colspan="5" class="text-center py-4 text-gray-400">Nenhuma escala cadastrada.</td></tr>';
        return;
      }

      tbody.innerHTML = data
        .map(
          (row) => `
        <tr>
          <td class="px-4 py-2">${row.funcionario}</td>
          <td class="px-4 py-2">${row.turno}</td>
          <td class="px-4 py-2">${row.data}</td>
          <td class="px-4 py-2 font-semibold ${
            row.status === "Ativo"
              ? "text-green-600"
              : row.status === "Substituto"
              ? "text-yellow-600"
              : "text-red-600"
          }">${row.status}</td>
          <td class="px-4 py-2 text-right">
            <button class="btn-outline text-sm delete-btn" data-id="${row.id}">🗑️</button>
          </td>
        </tr>`
        )
        .join("");

      tbody.querySelectorAll(".delete-btn").forEach((btn) =>
        btn.addEventListener("click", () => excluirEscala(btn.dataset.id))
      );
    }

    async function excluirEscala(id) {
      if (!confirm("Deseja realmente excluir esta escala?")) return;
      const res = await fetch(`/escalas/api/${id}`, { method: "DELETE" }).then((r) => r.json());
      if (res.ok) {
        toast("🗑️ Escala removida!");
        carregarEscalas();
      } else toast("❌ " + (res.error || "Erro ao excluir."));
    }
  }

  // ===============================================
  // 📊 6. Painel BI Dinâmico
  // ===============================================
  if (window.location.pathname === "/") {
    const chartContainer = document.getElementById("chart-bi");
    const kpiCards = document.querySelectorAll(".card");

    fetch("/escalas/api/dashboard")
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then(({ kpis, grafico }) => {
        if (kpiCards.length >= 3) {
          kpiCards[0].querySelector("p.text-4xl").textContent = kpis.alocados;
          kpiCards[1].querySelector("p.text-4xl").textContent = kpis.vagos;
          kpiCards[2].querySelector("p.text-4xl").textContent = kpis.substituicoes;
        }

        const data = [
          {
            x: grafico.dias,
            y: grafico.alocados,
            name: "Alocados",
            type: "bar",
            marker: { color: "#4f46e5" },
          },
          {
            x: grafico.dias,
            y: grafico.vagos,
            name: "Vagos",
            type: "bar",
            marker: { color: "#ef4444" },
          },
          {
            x: grafico.dias,
            y: grafico.substituicoes,
            name: "Substituições",
            type: "bar",
            marker: { color: "#f59e0b" },
          },
        ];

        const layout = {
          barmode: "group",
          title: `Produtividade Geral - ${kpis.produtividade}%`,
          plot_bgcolor: "transparent",
          paper_bgcolor: "transparent",
          font: { color: "#6b7280" },
          xaxis: { title: "Dias" },
          yaxis: { title: "Quantidade" },
          margin: { t: 50, l: 50, r: 30, b: 50 },
        };

        Plotly.newPlot("chart-bi", data, layout, { responsive: true });
      })
      .catch(() => {
        if (chartContainer)
          chartContainer.innerHTML =
            '<div class="text-center py-8 text-gray-500 dark:text-gray-400">⚠️ Erro ao carregar dados do BI.</div>';
      });
  }
});

// =====================================================
// 🔔 Toast e Animações Globais
// =====================================================
function toast(message) {
  const t = document.createElement("div");
  t.className =
    "fixed bottom-5 right-5 bg-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg text-sm fade-in";
  t.textContent = message;
  document.body.appendChild(t);
  setTimeout(() => {
    t.classList.add("fade-out");
    setTimeout(() => t.remove(), 300);
  }, 2000);
}

document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in");
});

window.addEventListener("pageshow", () => {
  document.body.classList.remove("fade-out");
});
