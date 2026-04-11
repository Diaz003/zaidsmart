/* ── Agentes UI · app.js (Proyectos) ─────────────────────── */

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

let currentProjectId = null;
let previousTaskIds = new Set();
let pollInterval = null;
let isSidebarOpen = false;

/* ── Mobile Sidebar Logic ───────────────────────────────── */
function toggleSidebar(force) {
  const body = document.body;
  isSidebarOpen = (force !== undefined) ? force : !isSidebarOpen;
  
  if (isSidebarOpen) {
    body.classList.add("sidebar-active");
  } else {
    body.classList.remove("sidebar-active");
  }
}

/* ── Escape HTML ─────────────────────────────────────────── */
function esc(text) {
  return String(text ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* ── Models (Cerebros) ───────────────────────────────────── */
/* ── Terminal System ─────────────────────────────────────── */
function sysLog(msg) {
  const term = $("#terminal-content");
  if (!term) return;

  // Traducir estados técnicos a algo amigable
  let icon = "⚙️";
  let tag = "SISTEMA";
  let cleanMsg = msg;

  if (msg.includes("Action:")) { icon = "🧠"; tag = "PENSANDO"; }
  if (msg.includes("Delegate") || msg.includes("Delegat")) { icon = "🤝"; tag = "DELEGANDO"; }
  if (msg.includes("Final Answer")) { icon = "✨"; tag = "FINALIZADO"; }
  if (msg.includes("Error")) { icon = "❌"; tag = "ERROR"; }

  cleanMsg = msg
    .replace(/<tool_call>[\s\S]*?<\/tool_call>/gi, "")
    .replace(/<scratchpad>[\s\S]*?<\/scratchpad>/gi, "")
    .replace(/Action:|Final Answer:|Thought:/gi, "")
    .trim();

  if (!cleanMsg) return;
  if (cleanMsg.length > 200) cleanMsg = cleanMsg.substring(0, 197) + "...";

  const time = new Date().toLocaleTimeString();
  const div = document.createElement("div");
  div.className = "term-line";
  div.innerHTML = `
    <span style="color:#666">[${time}]</span> 
    <span class="term-tag">${tag}</span>
    <span class="term-icon">${icon}</span> 
    ${esc(cleanMsg)}
  `;
  term.appendChild(div);
  term.scrollTop = term.scrollHeight;
}

/* ── Models (Cerebros) Scan ───────────────────────────────── */
async function loadModels(force = false) {
  const select = $("#model-select");
  const brainList = $("#active-brains-list");
  
  sysLog(force ? "Iniciando escaneo forzado de OpenRouter..." : "Sincronizando modelos con el servidor...");
  if(brainList) brainList.innerHTML = '<span class="scanning-text">Escaneando red...</span>';
  
  try {
    const res = await fetch(`/api/models/scan${force ? '?force=true' : ''}`);
    const models = await res.json();
    
    if (models.length > 0) {
      // Poblar Dropdown
      select.innerHTML = models.map(m => {
        const toolIcon = m.supports_tools ? "🛠️" : "💬";
        const selected = (m.id === "openrouter/free") ? "selected" : "";
        return `<option value="${esc(m.id)}" ${selected}>${toolIcon} ${esc(m.name)}</option>`;
      }).join("");

      // Poblar Panel Lateral
      if(brainList) {
        brainList.innerHTML = models.slice(0, 10).map(m => `
          <div class="brain-item" title="${esc(m.description)}">
            <span class="brain-id">${esc(m.id.split('/')[1] || m.id)}</span>
            <div class="brain-status">
              <span class="status-dot ${m.supports_tools ? 'online' : 'warn'}"></span>
              <span style="color:var(--text-dim); font-size:10px;">${Math.round(m.context_length/1000)}k</span>
            </div>
          </div>
        `).join("");
      }
      
      sysLog(`Localizados ${models.length} cerebros operativos.`);
      updateModelInfo();
    }
  } catch(e) {
    sysLog("ERROR: Fallo al conectar con el scanner de modelos.");
    select.innerHTML = `<option value="openrouter/free">openrouter/free (Fallback)</option>`;
  }
}

function updateModelInfo() {
  const select = $("#model-select");
  const hint = $("#model-info-text");
  const val = select.value;
  if(val === "openrouter/free") {
    hint.innerHTML = "✨ <b>Router Inteligente:</b> Elige el mejor modelo disponible.";
  } else {
    hint.innerHTML = `Cerebro seleccionado: <code>${val}</code>`;
  }
}


function statusIcon(s) {
  switch (s) {
    case "queued":  return "⏳";
    case "running": return "⚡";
    case "done":    return "✅";
    case "error":   return "❌";
    default:        return "❓";
  }
}

function timeAgo(ts) {
  if (!ts) return "";
  const diff = (Date.now() - new Date(ts + "Z").getTime()) / 1000;
  if (diff < 60)   return "hace unos segundos";
  if (diff < 3600) return `hace ${Math.floor(diff / 60)} min`;
  if (diff < 86400) return `hace ${Math.floor(diff / 3600)} h`;
  return new Date(ts).toLocaleDateString("es-ES");
}

/* ── Proyectos ───────────────────────────────────────────── */

async function loadProjects() {
  try {
    const res = await fetch("/projects");
    const projects = await res.json();
    
    const box = $("#projects-list");
    if (!projects.length) {
      box.innerHTML = `<p class="empty-msg-small">No hay proyectos.</p>`;
      if (!currentProjectId) showNoProjectView();
      return;
    }

    box.innerHTML = projects.map(p => {
      const displayPath = p.output_path || `output/${p.name.replace(/[^a-zA-Z0-9_\-]/g, "_")}`;
      return `
      <div class="project-item ${p.id === currentProjectId ? 'active' : ''}" data-id="${esc(p.id)}">
        <span class="project-icon">📂</span>
        <div style="flex: 1; min-width: 0;">
          <div class="project-name">${esc(p.name)}</div>
          <div style="font-size: 0.65rem; color: var(--text-dim); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${esc(displayPath)}">${esc(displayPath)}</div>
        </div>
      </div>
      `;
    }).join("");

    $$(".project-item").forEach(item => {
      item.addEventListener("click", () => selectProject(item.dataset.id, item.querySelector('.project-name').textContent));
    });

    if (!currentProjectId && projects.length > 0) {
      selectProject(projects[0].id, projects[0].name);
    }
  } catch (e) {
    console.error("Error loading projects:", e);
  }
}

async function createProject(name = null) {
  const pName = name || prompt("Nombre del nuevo proyecto:");
  if (!pName || !pName.trim()) return;

  const path = prompt("📂 Rutas de Resultados (Opcional):\n\nEscribe la ruta completa donde guardar los archivos de este proyecto en tu PC.\n\nEjemplo: /home/zaid/Escritorio/mi_juego\n(Déjalo en blanco para usar la carpeta por defecto de la app).");

  try {
    const res = await fetch("/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: pName.trim(), output_path: path || "" })
    });
    const data = await res.json();
    if (data.ok) {
      await loadProjects();
      selectProject(data.project_id, data.name);
    }
  } catch (e) {
    console.error("Error creating project:", e);
    alert("Error al crear proyecto");
  }
}

async function deleteCurrentProject() {
  if (!currentProjectId) return;
  if (!confirm("¿Seguro que quieres borrar este proyecto y todas sus tareas?")) return;

  try {
    await fetch(`/projects/${currentProjectId}`, { method: "DELETE" });
    currentProjectId = null;
    previousTaskIds.clear();
    showNoProjectView();
    loadProjects();
  } catch (e) {
    console.error("Error deleting project:", e);
  }
}

function selectProject(id, name) {
  currentProjectId = id;
  previousTaskIds.clear();
  
  // UI updates
  $$(".project-item").forEach(el => el.classList.remove('active'));
  const activeEl = $(`.project-item[data-id="${id}"]`);
  if (activeEl) activeEl.classList.add('active');

  showProjectView(name);
  loadTasks();

  if (pollInterval) clearInterval(pollInterval);
  pollInterval = setInterval(loadTasks, 2500);
  
  toggleSidebar(false); // Cerrar menú en móvil al elegir proyecto
}

function showNoProjectView() {
  $("#no-project-view").style.display = "flex";
  $("#project-view").style.display = "none";
  $("#current-project-badge").style.display = "none";
  if($("#btn-delete-project")) $("#btn-delete-project").style.display = "none";
  if (pollInterval) clearInterval(pollInterval);
}

function showProjectView(name) {
  $("#no-project-view").style.display = "none";
  $("#project-view").style.display = "block";
  const badge = $("#current-project-badge");
  badge.textContent = name;
  badge.style.display = "inline-flex";
  if($("#btn-delete-project")) $("#btn-delete-project").style.display = "inline-flex";
}

/* ── Tareas ──────────────────────────────────────────────── */

function renderTasks(tasks) {
  const box = $("#tasks-list");
  if (!tasks.length) {
    box.innerHTML = `<p class="empty-msg">Todavía no hay tareas en este proyecto. ¡Lanza una! 🚀</p>`;
    return;
  }

  // 1. Guardar el estado de los desplegables (abierto/cerrado)
  const openStates = {};
  box.querySelectorAll(".task-card").forEach(card => {
    const id = card.dataset.id;
    const resDetails = card.querySelector(".details-result");
    const logDetails = card.querySelector(".details-logs");
    openStates[id] = {
      result: resDetails ? resDetails.open : true, // Por defecto abierto
      logs: logDetails ? logDetails.open : false   // Por defecto cerrado
    };
  });

  box.innerHTML = tasks.map((t) => {
    const isNew = !previousTaskIds.has(t.task_id);
    let latestLog = "";
    let isDelegating = false;
    if (t.status === "running" && t.logs) {
      const lines = t.logs.trim().split("\n");
      latestLog = lines[lines.length - 1]; // Conseguir el último log para el progreso
      if (latestLog && (latestLog.includes("Delegat") || latestLog.includes("Action:") || latestLog.includes("Interacción"))) {
        isDelegating = true;
      }
    }

    // 2. Recuperar el estado o usar los valores por defecto
    const state = openStates[t.task_id] || { result: true, logs: false };

    return `
    <div class="task-card ${isNew ? "task-enter" : ""}" data-id="${esc(t.task_id)}">
      <div class="task-header">
        <div class="task-agent">
          <span class="agent-icon">${statusIcon(t.status)}</span>
          <span class="agent-name">${esc(t.agent_name)}</span>
        </div>
        <span class="badge badge--${t.status}">${esc(t.status)}</span>
      </div>
      <p class="task-desc">${esc(t.description)}</p>
      
      <!-- Barra de Progreso Dinámica -->
      <div class="progress-info">
        <span>${t.status === 'running' ? '<span class="ia-pulse"></span> Procesando...' : 'Estado'}</span>
        <span class="progress-percent">${t.progress || 0}%</span>
      </div>
      <div class="progress-container">
        <div class="progress-bar" style="width: ${t.progress || 0}%"></div>
      </div>

      <div class="task-meta">${timeAgo(t.updated_at)}</div>
      
      ${latestLog ? `<div class="progress-indicator ${isDelegating ? 'delegate-glow' : ''}"><span class="spinner">⚙️</span> <i>${esc(latestLog)}</i></div>` : ""}

      ${t.result ? `<details class="task-details details-result" ${state.result ? "open" : ""}><summary>Resultado Final</summary><pre>${esc(t.result)}</pre></details>` : ""}
      ${t.logs ? `<details class="task-details details-logs" ${state.logs ? "open" : ""}><summary>Ver Pensamientos (Logs)</summary><pre>${esc(t.logs)}</pre></details>` : ""}
    </div>`;
  }).join("");

  previousTaskIds = new Set(tasks.map((t) => t.task_id));
}

async function loadTasks() {
  if (!currentProjectId) return;
  try {
    const res = await fetch(`/projects/${currentProjectId}/tasks`);
    if (res.ok) {
      const tasks = await res.json();
      
      // Enviar nuevos logs a la terminal del sistema
      tasks.forEach(t => {
        if (t.status === "running" && t.logs) {
          const lines = t.logs.trim().split("\n");
          const lastLine = lines[lines.length - 1];
          if (lastLine && lastLine !== lastSeenLogs[t.task_id]) {
            sysLog(`${t.agent_name.toUpperCase()}: ${lastLine}`);
            lastSeenLogs[t.task_id] = lastLine;
          }
        }
        if (t.status === "done" && lastSeenLogs[t.task_id] !== "COMPLETED") {
          sysLog(`SISTEMA: Tarea ${t.task_id.substring(0,8)} completada con éxito.`);
          lastSeenLogs[t.task_id] = "COMPLETED";
        }
        if (t.status === "error" && lastSeenLogs[t.task_id] !== "ERROR") {
          sysLog(`ERROR: Tarea ${t.task_id.substring(0,8)} falló.`);
          lastSeenLogs[t.task_id] = "ERROR";
        }
      });

      renderTasks(tasks);
    }
  } catch (e) {
    console.error("Error loading tasks:", e);
  }
}

// Variable para tracking de logs vistos
let lastSeenLogs = {};

async function createTask() {
  if (!currentProjectId) return;
  
  const agentName = $("#agent-select").value;
  const modelId = $("#model-select").value;
  const description = $("#task-desc").value.trim();
  const msg = $("#create-msg");
  const btn = $("#create-btn");

  if (!description) {
    msg.textContent = "⚠️ Escribe una descripción primero.";
    msg.className = "form-msg form-msg--warn";
    return;
  }

  btn.disabled = true;
  btn.textContent = "Enviando…";
  msg.textContent = "";

  try {
    const res = await fetch(`/projects/${currentProjectId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ agent_name: agentName, model_id: modelId, description }),
    });
    const data = await res.json();

    msg.textContent = `✅ Tarea creada · ${data.task_id.slice(0, 8)}…`;
    msg.className = "form-msg form-msg--ok";
    $("#task-desc").value = "";

    await loadTasks();
  } catch (e) {
    msg.textContent = "❌ Error al crear la tarea.";
    msg.className = "form-msg form-msg--err";
    console.error(e);
  } finally {
    btn.disabled = false;
    btn.textContent = "🚀 Lanzar tarea";
  }
}

/* ── Init ────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  loadModels(); // Llenar el selector de modelos
  
  const modelSelect = $("#model-select");
  if(modelSelect) modelSelect.addEventListener("change", updateModelInfo);

  $("#create-btn").addEventListener("click", createTask);
  $("#btn-new-project").addEventListener("click", () => createProject());
  $("#btn-create-first").addEventListener("click", () => createProject());
  $("#btn-delete-project").addEventListener("click", deleteCurrentProject);
  
  if ($("#btn-refresh-models")) {
    $("#btn-refresh-models").addEventListener("click", () => loadModels(true));
  }

  // Mobile Listeners
  if ($("#btn-mobile-menu")) {
    $("#btn-mobile-menu").addEventListener("click", () => toggleSidebar());
  }
  if ($("#mobile-overlay")) {
    $("#mobile-overlay").addEventListener("click", () => toggleSidebar(false));
  }

  $("#task-desc").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) createTask();
  });

  loadProjects();
});
