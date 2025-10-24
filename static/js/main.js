/* =========================================================
   ESCALA360 - Main JavaScript
   Interatividade e experiência do usuário (UX/UI)
   Autor: Anderson de Matos Guimarães
   Data: 24/10/2025
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  // ===============================================
  // 🌓 1. Modo Escuro Persistente (UX aprimorado)
  // ===============================================
  const html = document.documentElement;
  const toggle = document.querySelector("#darkToggle");
  const storedTheme = localStorage.getItem("theme");

  // Aplica o tema salvo
  if (storedTheme === "dark") html.classList.add("dark");
  if (storedTheme === "light") html.classList.remove("dark");

  // Evento de alternância
  if (toggle) {
    toggle.addEventListener("click", () => {
      html.classList.toggle("dark");
      const isDark = html.classList.contains("dark");
      localStorage.setItem("theme", isDark ? "dark" : "light");

      // feedback visual
      const mode = isDark ? "🌙 Modo escuro ativado" : "☀️ Modo claro ativado";
      toast(mode);
    });
  }

  // ===============================================
  // 🔄 2. Animação de carregamento ao trocar de rota
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
  // 📊 3. Carregamento dinâmico de dados (tabelas e BI)
  // ===============================================
  if (window.location.pathname === "/escalas") {
    fetch("/api/escalas")
      .then((r) => r.json())
      .then((data) => renderEscalas(data))
      .catch(() => console.warn("Nenhum dado encontrado para /escalas"));
  }

  // ===============================================
  // 📈 4. Placeholder para gráficos (Plotly, futuramente)
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
// ⚙️ Função auxiliar: renderiza tabela de escalas
// =====================================================
function renderEscalas(data) {
  const tbody = document.querySelector("#tabela-escalas tbody");
  if (!tbody) return;

  tbody.innerHTML = data
    .map(
      (row) => `
    <tr class="hover:bg-indigo-50 dark:hover:bg-indigo-900 transition">
      <td class="px-4 py-2">${row.servidor}</td>
      <td class="px-4 py-2">${row.turno}</td>
      <td class="px-4 py-2 text-${
        row.status === "Ativo" ? "green" : "yellow"
      }-600 font-semibold">${row.status}</td>
      <td class="px-4 py-2 text-right">
        <button class="btn-outline text-sm">Editar</button>
      </td>
    </tr>`
    )
    .join("");
}

// =====================================================
// 🔔 Função auxiliar: toast minimalista
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

// =====================================================
// ✨ Animações de entrada e saída global
// =====================================================
document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in");
});

window.addEventListener("pageshow", () => {
  document.body.classList.remove("fade-out");
});
    