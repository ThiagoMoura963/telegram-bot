import { API_URL } from "./config.js";
import { agentValidator } from "./validators/agentValidator.js";
const logoutBtn = document.querySelector(".exit-btn");

let currentEditingAgentId = null;

let agents = [];

function cleanErrors() {
  document.querySelectorAll(".error-text").forEach((el) => {
    el.textContent = "";
  });
  document.querySelectorAll(".invalid").forEach((el) => {
    el.classList.remove("invalid");
  });
}

function showErrors(errors) {
  cleanErrors();

  Object.keys(errors).forEach((key) => {
    const errorText = document.getElementById(`${key}-error`);
    if (errorText) {
      errorText.textContent = errors[key];
    }

    const inputField = document.getElementById(key);
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
                <button class="config-card-btn" onclick="configAgent(${agent.id})">
                    <i class="fa-solid fa-gear"></i> Configurar
                </button>
            </div>
        </div>
    `;
}

function closeModal() {
  const buttons = document.querySelectorAll(".cancel-btn, close-x");
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

  document.getElementById("fileListAdd").innerHTML = "";

  modal.showModal();

  switchTab("tab-general-add", modal);

  saveBtn.onclick = async function (e) {
    e.preventDefault();

    const uploadedFiles = [];
    document.querySelectorAll("#fileListAdd .file-name").forEach((el) => {
      uploadedFiles.push(el.innerText);
    });

    const name = document.getElementById("name").value;
    const instruction = document.getElementById("instruction").value;
    const token = document.getElementById("tokenTelegram").value;
    const description = document.getElementById("description").value;

    const errors = agentValidator.validate(name, instruction, token);

    if (Object.keys(errors).length) {
      showErrors(errors);
      return;
    }

    const agentData = {
      name: name,
      description: description,
      system_prompt: instruction,
      telegram_token: token,
    };

    saveBtn.classList.add("loading");
    saveBtn.disabled = true;

    try {
      const response = await fetch(`${API_URL}/api/v1/agent`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(agentData),
        credentials: "include",
      });

      const result = await response.json();

      if (!response.ok) {
        saveBtn.classList.remove("loading");
        saveBtn.disabled = false;

        if (response.status === 400 && typeof result.detail === "object") {
          const { field, message } = result.detail;
          const errorObj = {};
          errorObj[field] = message;
          showErrors(errorObj);
          return;
        }

        throw new Error(response.detail || "Erro interno no servidor.");
      }

      agents.push(result);
      renderAgents(agents);
      modal.close();
    } catch (error) {
      console.error("Falha ao salvar o agente:", error);

      saveBtn.classList.remove("loading");
      saveBtn.disabled = false;
    }
  };
}

function configAgent(id) {
  const agent = agents.find((a) => a.id === id);
  const modal = document.getElementById("modalConfig");

  if (agent) {
    document.getElementById("nameConfig").value = agent.nome;
    document.getElementById("descriptionConfig").value = agent.descricao;
    document.getElementById("instructionConfig").value = agent.instrucao;
    document.getElementById("tokenTelegramConfig").value = agent.token;

    const listConfig = document.getElementById("docsListConfig");
    listConfig.innerHTML = "";

    if (agent.arquivos) {
      agent.arquivos.forEach((fileName) => {
        const li = document.createElement("li");
        li.className = "file-item";
        li.innerHTML = `
              <i class="fa-regular fa-file-lines file-icon"></i>
              <div class="file-info">
                <div class="file-name">${fileName}</div>
                <div class="progress-container">
                  <span class="percent">Concluído</span>
                </div>
              </div>
              <i class="fa-solid fa-trash remove-file" onclick="removeFileFromAgent(${agent.id}, '${fileName}', this)"></i>
            `;
        listConfig.appendChild(li);
      });
    }

    currentEditingAgentId = id;

    modal.showModal();

    switchTab("tab-general-config", modal);

    document.getElementById("saveConfig").onclick = () => {
      saveAgent(agent);
      renderAgents();
      modal.close();
    };
  }
}

function removeFileFromAgent(agentId, fileName, element) {
  const agent = agents.find((a) => a.id === agentId);
  if (agent) {
    agent.arquivos = agent.arquivos.filter((f) => f !== fileName);
    element.parentElement.remove();
  }
}

function renderAgents(agents = []) {
  const grid = document.querySelector("#gridAgents");
  grid.innerHTML = "";

  agents.forEach((agent) => {
    const card = createCardHTML(agent);
    grid.insertAdjacentHTML("beforeend", card);
  });
}

async function logout() {
  try {
    const response = await fetch(`${API_URL}/api/v1/auth/logout`, {
      method: "POST",
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
      credentials: "include",
    });

    if (!response.ok) throw new Error("Falha ao processar logout.");

    window.location.href = "login.html";
  } catch (error) {
    console.error("Erro no logout:", error);
  }
}

logoutBtn.addEventListener("click", logout);

window.configAgent = configAgent;
window.addAgent = addAgent;
window.switchTab = switchTab;
window.removeFileFromAgent = removeFileFromAgent;

document.addEventListener("DOMContentLoaded", async function () {
  try {
    console.log("API URL:", API_URL);
    const response = await fetch(`${API_URL}/api/v1/agent`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("Falha ao buscar agentes.");
    }

    if (response.status === 401) {
      window.location.href = "login.html";
      return;
    }

    const result = await response.json();
    agents = result.agents;
    renderAgents(agents);
  } catch (error) {
    console.error("Erro ao carregar agentes:", error);
  }

  closeModal();
});

renderAgents();
