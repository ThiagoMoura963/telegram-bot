/**
 * @param {string} dropZoneId
 * @param {string} fileInputId
 * @param {string} fileListId
 */

import { currentEditingAgentId, agents, addPendingFiles, renderPendingFiles } from "./dashboard.js";

function initUploadBehavior(dropZoneId, fileInputId, fileListId) {
  const dropZone = document.getElementById(dropZoneId);
  const fileInput = document.getElementById(fileInputId);
  const fileList = document.getElementById(fileListId);

  if (!dropZone || !fileInput || !fileList) return;

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.add("drag-over");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.remove("drag-over");
    });
  });

  dropZone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    handleFiles(files, fileList);
  });

  fileInput.addEventListener("change", () => {
    handleFiles(fileInput.files, fileList);
  });
}

function handleFiles(files, listElement) {
  const filesArray = Array.from(files);

  if (listElement.id === "fileListAdd") {
    addPendingFiles(filesArray);
    renderPendingFiles();
  }
  else{
    renderConfigFiles(filesArray, listElement)
  }

  const inputId = listElement.id === "fileListAdd" ? "docsFileAdd" : "docsFileConfig";
  const input = document.getElementById(inputId);
  if (input) input.value = "";
}

function renderConfigFiles(filesArray, listElement) {
  filesArray.forEach(file => {
    const li = document.createElement("li");
    li.className = "file-item";
    li.innerHTML = `
      <li class="file-item">
        <i class="fa-regular fa-file-lines file-icon-list"></i>

        <div class="file-info">
          <div class="file-name">${file.name}</div>
        </div>

        <i class="fa-solid fa-xmark remove-file"
          onclick="removePendingFile('${file.name}', this)">
        </i>
      </li>
    `;

    listElement.appendChild(li);

    if (currentEditingAgentId) {
      const agent = agents.find((a) => a.id === currentEditingAgentId);

      if (agent) {
        if (!agent.arquivos) {
          agent.arquivos = [];
        }

        if (!agent.arquivos.includes(file.name)) {
          agent.arquivos.push(file.name);
        }
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initUploadBehavior("dropZoneAdd", "docsFileAdd", "fileListAdd");
  initUploadBehavior("dropZoneConfig", "docsFileConfig", "docsListConfig");
});
