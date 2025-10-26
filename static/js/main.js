/* =========================================================
   ESCALA360 - Main JavaScript
   Interatividade e experiência do usuário (UX/UI)
   Autor: Anderson de Matos Guimarães
   Data: 27/10/2025
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
  // 🔄 2. Animação de transição entre páginas
  // ===============================================
  const links = document.querySelectorAll("a[href]");
  links.forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (!href.startsWith("#") && !href.startsWith("javascript")) {
        document.body.classList.add("fade-out");
        setTimeout(() => (window.location = href), 250);
        e.preventDefault();
      }
    });
  });

  // ===============================================
  // 📊 3. CRUD - Escalas
  // ===============================================
  if (window.location.pathname === "/escalas") {
    const form = document.querySelector("#form-escala");
    const tbody = document.querySelector("#tabela-escalas tbody");

    // 🔹 Carrega as escalas ao iniciar
    carregarEscalas();

    // 🔹 Submissão do formulário (CREATE)
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const payload = {
        funcionario_id: form.funcionario_id.value,
        turno_id: form.turno_id.value,
        data: form.data.value,
        status: form.status.value,
      };

      fetch("/escalas/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((r) => r.json())
        .then((res) => {
          if (res.ok) {
            toast("✅ Escala cadastrada com sucesso!");
            form.reset();
            carregarEscalas();
          } else {
            throw new Error(res.error || "Erro desconhecido");
          }
        })
        .catch((err) => toast("❌ Erro: " + err.message));
    });

    // 🔹 Função para carregar escalas
    function carregarEscalas() {
      fetch("/escalas/api")
        .then((r) => r.json())
        .then((data) => renderEscalas(data))
        .catch(() => toast("⚠️ Não foi possível carregar as escalas."));
    }

    // 🔹 Renderização das escalas na tabela
    function renderEscalas(data) {
      if (!tbody) return;
      if (!data.length) {
        tbody.innerHTML =
          '<tr><td colspan="5" class="text-center py-4 text-gray-400">Nenhuma escala cadastrada.</td></tr>';
        return;
      }

      tbody.innerHTML = data
        .map(
          (row) => `
        <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900 transition">
          <td class="px-4 py-2">${row.funcionario}</td>
          <td class="px-4 py-2">${row.turno}</td>
          <td class="px-4 py-2">${row.data}</td>
          <td class="px-4 py-2 font-semibold text-${
            row.status === "Ativo"
              ? "green"
              : row.status === "Substituto"
              ? "yellow"
              : "red"
          }-600">${row.status}</td>
          <td class="px-4 py-2 text-right space-x-2">
            <button class="btn-outline text-sm edit-btn" data-id="${
              row.id
            }">✏️ Editar</button>
            <button class="btn-outline text-sm delete-btn text-red-600" data-id="${
              row.id
            }">🗑️ Excluir</button>
          </td>
        </tr>`
        )
        .join("");

      // Botões de ação
      tbody.querySelectorAll(".edit-btn").forEach((btn) =>
        btn.addEventListener("click", () => abrirModalEdicao(btn.dataset.id))
      );

      tbody.querySelectorAll(".delete-btn").forEach((btn) =>
        btn.addEventListener("click", () => excluirEscala(btn.dataset.id))
      );
    }

    // 🔹 Modal de Edição (UPDATE)
    function abrirModalEdicao(id) {
      fetch(`/escalas/api`)
        .then((r) => r.json())
        .then((escalas) => {
          const escala = escalas.find((e) => e.id == id);
          if (!escala) return toast("⚠️ Escala não encontrada.");

          const modal = document.createElement("div");
          modal.className =
            "fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 fade-in";
          modal.innerHTML = `
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg w-96 relative">
              <h2 class="text-lg font-semibold mb-4 text-indigo-600">Editar Escala</h2>
              <form id="form-edit-escala">
                <label>Data</label>
                <input type="date" name="data" value="${escala.data}" class="w-full p-2 mb-2 rounded border dark:bg-gray-700">
                <label>Status</label>
                <select name="status" class="w-full p-2 mb-2 rounded border dark:bg-gray-700">
                  <option value="Ativo" ${escala.status === "Ativo" ? "selected" : ""}>Ativo</option>
                  <option value="Substituto" ${escala.status === "Substituto" ? "selected" : ""}>Substituto</option>
                  <option value="Vago" ${escala.status === "Vago" ? "selected" : ""}>Vago</option>
                </select>
                <div class="text-right mt-4 space-x-2">
                  <button type="button" id="cancelar-edicao" class="btn-outline">Cancelar</button>
                  <button type="submit" class="btn-outline bg-indigo-600 text-white">Salvar</button>
                </div>
              </form>
            </div>
          `;
          document.body.appendChild(modal);

          modal.querySelector("#cancelar-edicao").onclick = () => modal.remove();

          modal.querySelector("#form-edit-escala").onsubmit = (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const payload = {
              data: formData.get("data"),
              status: formData.get("status"),
            };

            fetch(`/escalas/api/${id}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            })
              .then((r) => r.json())
              .then((res) => {
                if (res.ok) {
                  toast("✅ Escala atualizada com sucesso!");
                  modal.remove();
                  carregarEscalas();
                } else {
                  throw new Error(res.error);
                }
              })
              .catch((err) => toast("❌ Erro: " + err.message));
          };
        });
    }

    // 🔹 Exclusão (DELETE)
    function excluirEscala(id) {
      if (!confirm("Deseja realmente excluir esta escala?")) return;

      fetch(`/escalas/api/${id}`, { method: "DELETE" })
        .then((r) => r.json())
        .then((res) => {
          if (res.ok) {
            toast("🗑️ Escala excluída com sucesso!");
            carregarEscalas();
          } else {
            throw new Error(res.error);
          }
        })
        .catch((err) => toast("❌ Erro: " + err.message));
    }
  }

  // ===============================================
  // 📈 4. Painel BI Dinâmico
  // ===============================================
  if (window.location.pathname === "/") {
    const chartContainer = document.getElementById("chart-bi");
    const kpiCards = document.querySelectorAll(".card");

    fetch("/escalas/api/dashboard")
      .then((r) => r.json())
      .then((dados) => {
        const { kpis, grafico } = dados;

        // Atualiza KPIs
        const [alocados, vagos, substituicoes, produtividade] = [
          kpis.alocados,
          kpis.vagos,
          kpis.substituicoes,
          kpis.produtividade,
        ];

        if (kpiCards.length >= 3) {
          kpiCards[0].querySelector("p.text-4xl").textContent = alocados;
          kpiCards[1].querySelector("p.text-4xl").textContent = vagos;
          kpiCards[2].querySelector("p.text-4xl").textContent = substituicoes;
        }

        // Renderiza gráfico Plotly
        if (chartContainer) {
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
            title: `Produtividade Geral - ${produtividade}%`,
            plot_bgcolor: "transparent",
            paper_bgcolor: "transparent",
            font: { color: "#6b7280" },
            xaxis: { title: "Dias" },
            yaxis: { title: "Quantidade" },
            margin: { t: 50, l: 50, r: 30, b: 50 },
          };

          Plotly.newPlot("chart-bi", data, layout, { responsive: true });
        }
      })
      .catch(() => {
        if (chartContainer) {
          chartContainer.innerHTML =
            '<div class="text-center py-8 text-gray-500 dark:text-gray-400">⚠️ Erro ao carregar dados do BI.</div>';
        }
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
