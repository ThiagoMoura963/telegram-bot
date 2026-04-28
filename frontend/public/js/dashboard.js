import { API_URL } from "./config.js";
import { agentValidator } from "./validators/agentValidator.js";

const logoutBtn = document.querySelector(".exit-btn");
let currentEditingAgentId = null;
let agents = [];

function cleanErrors(container = document) {
  container.querySelectorAll(".error-text").forEach((el) => {
    el.textContent = "";
  });
  container.querySelectorAll(".invalid").forEach((el) => {
    el.classList.remove("invalid");
  });
}

function showErrors(errors, suffix = "") {
  cleanErrors();

  Object.keys(errors).forEach((key) => {
    const targetId = suffix ? `${key}${suffix}` : key;

    const errorText = document.getElementById(`${targetId}-error`);
    if (errorText) {
      errorText.textContent = errors[key];
    }

    const inputField = document.getElementById(targetId);
    if (inputField) {
      inputField.classList.add("invalid");
    }
  });
}

function switchTab(tabId, event) {
  const targetEl = event.currentTarget || event;
  const modal = targetEl.closest("dialog");

  modal
    .querySelectorAll(".tab-content")
    .forEach((tab) => tab.classList.remove("active"));
  modal
    .querySelectorAll(".tab-btn")
    .forEach((btn) => btn.classList.remove("active"));

  document.getElementById(tabId).classList.add("active");
  const btn = modal.querySelector(`button[onclick*="${tabId}"]`);
  if (btn) btn.classList.add("active");
}

function createCardHTML(agent) {
  return `
        <div class="agent-card" data-id="${agent.id}">
            <div class="card-header">
                <div class="info">
                    <h3>${agent.name}</h3>
                </div>
            </div>
            <p class="card-desc">${agent.description || "Sem descrição"}</p>
            <div class="card-footer">
                <button class="config-card-btn" onclick="configAgent('${agent.id}')">
                    <i class="fa-solid fa-gear"></i> Configurar
                </button>
                <button class="delete-card-btn" onclick="deleteAgent('${agent.id}', event)">
                    <span class="btn-text"><i class="fa-solid fa-trash"></i> Deletar</span>
                    <div class="spinner"></div>
                </button>
            </div>
        </div>
    `;
}

function renderAgents(agentsList = agents) {
  const grid = document.querySelector("#gridAgents");
  grid.innerHTML = "";
  agentsList.forEach((agent) => {
    grid.insertAdjacentHTML("beforeend", createCardHTML(agent));
  });
}

function closeModal() {
  const buttons = document.querySelectorAll(".cancel-btn, .close-x");
  buttons.forEach((btn) => {
    btn.onclick = () => {
      const modal = btn.closest("dialog");
      modal
        .querySelectorAll('input[type="file"]')
        .forEach((input) => (input.value = ""));
      modal.close();
    };
  });
}

function addAgent() {
  const modal = document.getElementById("modalAgent");
  const form = modal.querySelector("form");
  const saveBtn = document.getElementById("saveAdd");

  form.reset();
  cleanErrors(modal);
  document.getElementById("fileListAdd").innerHTML = "";

  modal.showModal();
  switchTab("tab-general-add", modal);

  saveBtn.onclick = async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;
    const instruction = document.getElementById("instruction").value;
    const token = document.getElementById("tokenTelegram").value;

    const errors = agentValidator.validate(name, instruction, token);
    if (Object.keys(errors).length) {
      showErrors(errors);
      return;
    }

    const agentData = {
      name,
      description,
      system_prompt: instruction,
      telegram_token: token,
    };

    saveBtn.classList.add("loading");
    saveBtn.disabled = true;

    try {
      const response = await fetch(`${API_URL}/api/v1/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(agentData),
        credentials: "include",
      });

      const result = await response.json();

      if (!response.ok) {
        if (response.status === 400 && result.detail?.field) {
          const errorObj = { [result.detail.field]: result.detail.message };
          showErrors(errorObj);
          return;
        }
        throw new Error(result.detail || "Erro ao salvar agente");
      }

      agents.push(result);
      renderAgents();
      modal.close();
    } catch (error) {
      console.error("Falha ao salvar:", error);
      alert(error.message);
    } finally {
      saveBtn.classList.remove("loading");
      saveBtn.disabled = false;
    }
  };
}

function configAgent(id) {
  const agent = agents.find((a) => a.id === id);
  const modal = document.getElementById("modalConfig");

  if (agent) {
    cleanErrors(modal);

    document.getElementById("nameConfig").value = agent.name || "";
    document.getElementById("descriptionConfig").value =
      agent.description || "";
    document.getElementById("instructionConfig").value =
      agent.system_prompt || "";
    document.getElementById("tokenTelegramConfig").value =
      agent.telegram_token || "";
    document.getElementById("switchCheck").checked = !!agent.is_active;

    const listConfig = document.getElementById("docsListConfig");
    listConfig.innerHTML = "";
    if (agent.arquivos) {
      agent.arquivos.forEach((fileName) => {
        listConfig.insertAdjacentHTML(
          "beforeend",
          `
                    <li class="file-item">
                        <i class="fa-regular fa-file-lines file-icon"></i>
                        <div class="file-info">
                            <div class="file-name">${fileName}</div>
                            <div class="progress-container"><span class="percent">Concluído</span></div>
                        </div>
                        <i class="fa-solid fa-trash remove-file" onclick="removeFileFromAgent('${agent.id}', '${fileName}', this)"></i>
                    </li>`,
        );
      });
    }

    currentEditingAgentId = id;
    const saveBtn = document.getElementById("saveConfig");

    saveBtn.onclick = async (e) => {
      e.preventDefault();

      const name = document.getElementById("nameConfig").value;
      const description = document.getElementById("descriptionConfig").value;
      const instruction = document.getElementById("instructionConfig").value;
      const telegramToken = document.getElementById(
        "tokenTelegramConfig",
      ).value;
      const isActive = document.getElementById("switchCheck").checked;

      const errors = agentValidator.validate(name, instruction, telegramToken);
      if (Object.keys(errors).length) {
        showErrors(errors, "Config");
        return;
      }

      const updatedAgentData = {
        name,
        description,
        system_prompt: instruction,
        telegram_token: telegramToken,
        is_active: isActive,
      };

      saveBtn.classList.add("loading");
      saveBtn.disabled = true;

      try {
        const response = await fetch(`${API_URL}/api/v1/agent/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
          },
          body: JSON.stringify(updatedAgentData),
          credentials: "include",
        });

        const result = await response.json();

        if (!response.ok) {
          if (response.status === 400 && result.detail?.field) {
            const errorObj = { [result.detail.field]: result.detail.message };
            showErrors(errorObj, "Config");
            return;
          }
          throw new Error(result.detail || "Falha ao editar agente");
        }

        const index = agents.findIndex((a) => a.id === id);
        if (index !== -1) agents[index] = result;

        renderAgents();
        modal.close();
      } catch (error) {
        console.error("Erro no update:", error);
        alert(error.message);
      } finally {
        saveBtn.classList.remove("loading");
        saveBtn.disabled = false;
      }
    };

    modal.showModal();
    switchTab("tab-general-config", modal);
  }
}

async function deleteAgent(id, event) {
  if (!id) return;
  const btn = event.currentTarget;

  if (!confirm("Tem certeza que deseja deletar o agente?")) return;

  btn.classList.add("loading");
  btn.disabled = true;

  try {
    const response = await fetch(`${API_URL}/api/v1/agent/${id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    if (!response.ok) throw new Error("Erro ao deletar");

    agents = agents.filter((agent) => agent.id !== id);
    renderAgents();
  } catch (error) {
    console.error("Falha ao deletar:", error);
    alert("Não foi possível deletar o agente.");
  } finally {
    btn.classList.remove("loading");
    btn.disabled = false;
  }
}

function removeFileFromAgent(agentId, fileName, element) {
  const agent = agents.find((a) => a.id === agentId);
  if (agent && agent.arquivos) {
    agent.arquivos = agent.arquivos.filter((f) => f !== fileName);
    element.parentElement.remove();
  }
}

async function logout() {
  try {
    const response = await fetch(`${API_URL}/api/v1/auth/logout`, {
      method: "POST",
      headers: { "ngrok-skip-browser-warning": "true" },
      credentials: "include",
    });
    if (!response.ok) throw new Error("Falha no logout");
    window.location.href = "login.html";
  } catch (error) {
    console.error("Erro no logout:", error);
  }
}

window.configAgent = configAgent;
window.addAgent = addAgent;
window.deleteAgent = deleteAgent;
window.switchTab = switchTab;
window.removeFileFromAgent = removeFileFromAgent;

logoutBtn.addEventListener("click", logout);

document.addEventListener("DOMContentLoaded", async function () {
  try {
    const response = await fetch(`${API_URL}/api/v1/agent`, {
      method: "GET",
      headers: { "ngrok-skip-browser-warning": "true" },
      credentials: "include",
    });

    if (response.status === 401) {
      window.location.href = "login.html";
      return;
    }

    if (!response.ok) throw new Error("Falha ao buscar agentes");

    const result = await response.json();
    agents = result.agents || [];
    renderAgents();
  } catch (error) {
    console.error("Erro inicial:", error);
  }
  closeModal();
});
