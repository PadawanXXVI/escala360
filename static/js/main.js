/* =========================================================
   ESCALA360 - Main JavaScript
   Interatividade e experiência do usuário (UX/UI)
   Autor: Anderson de Matos Guimarães
   Data: 26/10/2025
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  // ===============================================
  // 🌓 1. Modo Escuro Persistente (UX aprimorado)
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
  // 🔄 2. Animação ao trocar de rota
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
  // 📊 3. Escalas
  // ===============================================
  if (window.location.pathname === "/escalas") {
    fetch("/escalas/api")
      .then((r) => r.json())
      .then((data) => renderEscalas(data))
      .catch(() => toast("⚠️ Falha ao carregar escalas."));
  }

  // ===============================================
  // 👥 4. Usuários
  // ===============================================
  if (window.location.pathname === "/usuarios") {
    const form = document.querySelector("#form-funcionario");
    const tbody = document.querySelector("#tabela-funcionarios tbody");

    fetch("/usuarios/api")
      .then((r) => r.json())
      .then((data) => renderFuncionarios(data))
      .catch(() => toast("⚠️ Não foi possível carregar os funcionários."));

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const payload = {
        nome: form.nome.value,
        cargo: form.cargo.value,
        email: form.email.value,
        ativo: form.ativo.checked,
      };

      fetch("/usuarios/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((r) => r.json())
        .then((res) => {
          if (res.ok) {
            toast("✅ Funcionário cadastrado!");
            form.reset();
            return fetch("/usuarios/api")
              .then((r) => r.json())
              .then(renderFuncionarios);
          }
          throw new Error(res.error || "Erro desconhecido");
        })
        .catch((err) => toast("❌ Erro: " + err.message));
    });
  }

  // ===============================================
  // ⏰ 5. Turnos
  // ===============================================
  if (window.location.pathname === "/turnos") {
    const form = document.querySelector("#form-turno");
    const tbody = document.querySelector("#tabela-turnos tbody");

    fetch("/turnos/api")
      .then((r) => r.json())
      .then((data) => renderTurnos(data))
      .catch(() => toast("⚠️ Não foi possível carregar os turnos."));

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const payload = {
        nome: form.nome.value,
        inicio: form.inicio.value,
        fim: form.fim.value,
      };

      fetch("/turnos/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((r) => r.json())
        .then((res) => {
          if (res.ok) {
            toast("✅ Turno cadastrado com sucesso!");
            form.reset();
            return fetch("/turnos/api")
              .then((r) => r.json())
              .then(renderTurnos);
          }
          throw new Error(res.error || "Erro desconhecido");
        })
        .catch((err) => toast("❌ Erro: " + err.message));
    });
  }

  // ===============================================
  // 📈 6. Painel BI (placeholder)
  // ===============================================
  if (window.location.pathname === "/") {
    const chartContainer = document.getElementById("chart-bi");
    if (chartContainer) {
      chartContainer.innerHTML = `
        <div class="text-center py-8 text-gray-500 dark:text-gray-400">
          <i class="fas fa-chart-line text-4xl mb-4"></i><br>
          Painel BI em desenvolvimento...
        </div>`;
    }
  }
});

// =====================================================
// ⚙️ Renderização: Escalas
// =====================================================
function renderEscalas(data) {
  const tbody = document.querySelector("#tabela-escalas tbody");
  if (!tbody) return;
  if (!data.length) {
    tbody.innerHTML =
      '<tr><td colspan="4" class="text-center py-4 text-gray-400">Nenhuma escala encontrada.</td></tr>';
    return;
  }
  tbody.innerHTML = data
    .map(
      (row) => `
      <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900 transition">
        <td class="px-4 py-2">${row.servidor}</td>
        <td class="px-4 py-2">${row.turno}</td>
        <td class="px-4 py-2 text-${
          row.status === "Ativo"
            ? "green"
            : row.status === "Substituto"
            ? "yellow"
            : "red"
        }-600 font-semibold">${row.status}</td>
        <td class="px-4 py-2 text-right">
          <button class="btn-outline text-sm">Editar</button>
        </td>
      </tr>`
    )
    .join("");
}

// =====================================================
// ⚙️ Renderização: Funcionários
// =====================================================
function renderFuncionarios(data) {
  const tbody = document.querySelector("#tabela-funcionarios tbody");
  if (!tbody) return;
  if (!data.length) {
    tbody.innerHTML =
      '<tr><td colspan="4" class="text-center py-4 text-gray-400">Nenhum funcionário encontrado.</td></tr>';
    return;
  }
  tbody.innerHTML = data
    .map(
      (f) => `
      <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900 transition">
        <td class="px-4 py-2">${f.nome}</td>
        <td class="px-4 py-2">${f.cargo}</td>
        <td class="px-4 py-2">${f.email}</td>
        <td class="px-4 py-2 text-center">
          <span class="px-2 py-1 rounded-full text-xs font-semibold ${
            f.ativo
              ? "bg-green-100 text-green-700 dark:bg-green-800 dark:text-green-200"
              : "bg-red-100 text-red-700 dark:bg-red-800 dark:text-red-200"
          }">${f.ativo ? "Ativo" : "Inativo"}</span>
        </td>
      </tr>`
    )
    .join("");
}

// =====================================================
// ⚙️ Renderização: Turnos
// =====================================================
function renderTurnos(data) {
  const tbody = document.querySelector("#tabela-turnos tbody");
  if (!tbody) return;
  if (!data.length) {
    tbody.innerHTML =
      '<tr><td colspan="3" class="text-center py-4 text-gray-400">Nenhum turno cadastrado.</td></tr>';
    return;
  }
  tbody.innerHTML = data
    .map(
      (t) => `
      <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900 transition">
        <td class="px-4 py-2">${t.nome}</td>
        <td class="px-4 py-2 text-center">${t.inicio}</td>
        <td class="px-4 py-2 text-center">${t.fim}</td>
      </tr>`
    )
    .join("");
}

// =====================================================
// 🔔 Toasts e animações globais
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
