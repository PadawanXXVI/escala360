/* =========================================================
   ESCALA360 - Main JavaScript (UI/UX Interactions)
   Autor: Anderson de Matos Guimarães
   Revisão: 02/11/2025
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  // =====================================================
  // 🌓 1. MODO ESCURO PERSISTENTE
  // =====================================================
  const html = document.documentElement;
  const toggle = document.querySelector("#darkToggle");
  const storedTheme = localStorage.getItem("theme");

  if (storedTheme === "dark") html.classList.add("dark");
  if (storedTheme === "light") html.classList.remove("dark");

  toggle?.addEventListener("click", () => {
    html.classList.toggle("dark");
    const isDark = html.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    toast(isDark ? "🌙 Modo escuro ativado" : "☀ Modo claro ativado", "info");
  });

  // =====================================================
  // 🔄 2. TRANSIÇÃO SUAVE ENTRE PÁGINAS
  // =====================================================
  document.querySelectorAll("a[href]").forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#") || href.startsWith("javascript")) return;
      document.body.classList.add("fade-out");
      e.preventDefault();
      setTimeout(() => (window.location = href), 250);
    });
  });

  // =====================================================
  // 👥 3. CRUD - PROFISSIONAIS
  // =====================================================
  if (window.location.pathname.includes("/profissionais")) {
    const form = document.querySelector("#form-profissional");
    const tbody = document.querySelector("#tabela-profissionais tbody");
    if (form && tbody) crudProfissionais(form, tbody);
  }

  // =====================================================
  // 🕒 4. CRUD - PLANTÕES
  // =====================================================
  if (window.location.pathname.includes("/plantoes")) {
    const form = document.querySelector("#form-plantao");
    const tbody = document.querySelector("#tabela-plantoes tbody");
    if (form && tbody) crudPlantoes(form, tbody);
  }

  // =====================================================
  // 📋 5. CRUD - ESCALAS
  // =====================================================
  if (window.location.pathname.includes("/escalas")) {
    const form = document.querySelector("#form-escala");
    const tbody = document.querySelector("#tabela-escalas tbody");
    if (form && tbody) crudEscalas(form, tbody);
  }

  // =====================================================
  // 📊 6. DASHBOARD (BI)
  // =====================================================
  if (window.location.pathname === "/" || window.location.pathname === "/index") {
    carregarPainelBI();
  }
});

// =====================================================
// 🔧 FUNÇÕES CRUD MODULARES
// =====================================================
async function crudProfissionais(form, tbody) {
  await carregarProfissionais();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      nome: form.nome.value.trim(),
      cargo: form.cargo.value.trim(),
      email: form.email.value.trim(),
      ativo: form.ativo.checked,
    };

    try {
      const res = await fetch("/profissionais/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then((r) => r.json());

      if (res.ok) {
        toast("✅ Profissional cadastrado!", "success");
        form.reset();
        carregarProfissionais();
      } else throw new Error(res.error || "Erro ao cadastrar profissional.");
    } catch (err) {
      toast("❌ " + err.message, "error");
    }
  });

  async function carregarProfissionais() {
    try {
      const data = await fetch("/profissionais/api").then((r) => r.json());
      render(data);
    } catch {
      toast("⚠ Falha ao carregar profissionais.", "warning");
    }
  }

  function render(data) {
    tbody.innerHTML = data.length
      ? data
          .map(
            (p) => `
            <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition">
              <td>${p.nome}</td>
              <td>${p.cargo || "—"}</td>
              <td>${p.email}</td>
              <td class="${p.ativo ? "text-green-600" : "text-red-600"}">${p.ativo ? "Ativo" : "Inativo"}</td>
            </tr>`
          )
          .join("")
      : <tr><td colspan="4" class="text-center py-4 text-gray-400">Nenhum profissional cadastrado.</td></tr>;
  }
}

async function crudPlantoes(form, tbody) {
  await carregarPlantoes();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      data: form.data.value,
      hora_inicio: form.hora_inicio.value,
      hora_fim: form.hora_fim.value,
      id_funcao: form.id_funcao.value,
      id_local: form.id_local.value,
    };

    try {
      const res = await fetch("/plantoes/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then((r) => r.json());

      if (res.ok) {
        toast("✅ Plantão cadastrado!", "success");
        form.reset();
        carregarPlantoes();
      } else throw new Error(res.error);
    } catch (err) {
      toast("❌ " + err.message, "error");
    }
  });

  async function carregarPlantoes() {
    try {
      const data = await fetch("/plantoes/api").then((r) => r.json());
      render(data);
    } catch {
      toast("⚠ Falha ao carregar plantões.", "warning");
    }
  }

  function render(data) {
    tbody.innerHTML = data.length
      ? data
          .map(
            (p) => `
            <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition">
              <td>${p.data}</td>
              <td>${p.hora_inicio} - ${p.hora_fim}</td>
              <td>${p.id_funcao}</td>
              <td>${p.id_local}</td>
              <td class="text-right">
                <button class="btn-outline text-sm delete-btn" data-id="${p.id}" title="Excluir">🗑</button>
              </td>
            </tr>`
          )
          .join("")
      : <tr><td colspan="5" class="text-center py-4 text-gray-400">Nenhum plantão cadastrado.</td></tr>;

    tbody.querySelectorAll(".delete-btn").forEach((btn) =>
      btn.addEventListener("click", () => excluir(btn.dataset.id))
    );
  }

  async function excluir(id) {
    if (!confirm("Deseja excluir este plantão?")) return;
    try {
      const res = await fetch(/plantoes/api/${id}, { method: "DELETE" }).then((r) => r.json());
      if (res.ok) {
        toast("🗑 Plantão excluído!", "success");
        carregarPlantoes();
      } else throw new Error(res.error);
    } catch {
      toast("❌ Erro ao excluir plantão.", "error");
    }
  }
}

async function crudEscalas(form, tbody) {
  await carregarEscalas();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      id_profissional: form.id_profissional.value,
      id_plantao: form.id_plantao.value,
      status: form.status.value,
    };

    try {
      const res = await fetch("/escalas/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then((r) => r.json());

      if (res.ok) {
        toast("✅ Escala cadastrada!", "success");
        form.reset();
        carregarEscalas();
      } else throw new Error(res.error);
    } catch (err) {
      toast("❌ " + err.message, "error");
    }
  });

  async function carregarEscalas() {
    try {
      const data = await fetch("/escalas/api").then((r) => r.json());
      render(data);
    } catch {
      toast("⚠ Falha ao carregar escalas.", "warning");
    }
  }

  function render(data) {
    tbody.innerHTML = data.length
      ? data
          .map(
            (e) => `
            <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition">
              <td>${e.profissional}</td>
              <td>${e.cargo}</td>
              <td>${e.data}</td>
              <td>${e.hora_inicio} - ${e.hora_fim}</td>
              <td>${e.status}</td>
            </tr>`
          )
          .join("")
      : <tr><td colspan="5" class="text-center py-4 text-gray-400">Nenhuma escala cadastrada.</td></tr>;
  }
}

// =====================================================
// 📈 7. DASHBOARD / BI
// =====================================================
function carregarPainelBI() {
  fetch("/escalas/api/dashboard")
    .then((r) => (r.ok ? r.json() : Promise.reject()))
    .then(({ kpis, grafico }) => {
      const data = [
        { x: grafico.dias, y: grafico.alocados, name: "Alocados", type: "bar", marker: { color: "#4f46e5" } },
        { x: grafico.dias, y: grafico.vagos, name: "Vagos", type: "bar", marker: { color: "#ef4444" } },
        { x: grafico.dias, y: grafico.substituicoes, name: "Substituições", type: "bar", marker: { color: "#f59e0b" } },
      ];
      Plotly.newPlot("chart-bi", data, {
        barmode: "group",
        title: Produtividade Geral - ${kpis.produtividade}%,
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent",
        font: { color: "#6b7280" },
        margin: { t: 50, l: 50, r: 30, b: 50 },
      });
    })
    .catch(() => {
      document.getElementById("chart-bi").innerHTML =
        '<div class="text-center py-8 text-gray-500 dark:text-gray-400">⚠ Erro ao carregar dados do BI.</div>';
    });
}

// =====================================================
// 🔔 TOAST GLOBAL
// =====================================================
function toast(message, type = "info") {
  const colors = {
    info: "bg-indigo-600",
    success: "bg-green-600",
    error: "bg-red-600",
    warning: "bg-yellow-500",
  };

  const t = document.createElement("div");
  t.className = toast fixed bottom-5 right-5 ${colors[type]} text-white px-4 py-2 rounded-lg shadow-lg text-sm fade-in;
  t.innerHTML = <span>${message}</span>;
  document.body.appendChild(t);

  setTimeout(() => {
    t.style.opacity = "0";
    setTimeout(() => t.remove(), 300);
  }, 2500);
}
