/**
* @param {string} dropZoneId
* @param {string} fileInputId
* @param {string} fileListId
 */

function initUploadBehavior(dropZoneId, fileInputId, fileListId) {
    const dropZone = document.getElementById(dropZoneId);
    const fileInput = document.getElementById(fileInputId);
    const fileList = document.getElementById(fileListId);

    if (!dropZone || !fileInput || !fileList) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'));
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'));
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        handleFiles(files, fileList);
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files, fileList);
    });
}

function handleFiles(files, listElement) {
    Array.from(files).forEach(file => {
        const fileId = 'file-' + Math.random().toString(36).substr(2, 9);
        const li = document.createElement('li');
        li.className = 'file-item';
        li.innerHTML = `
            <i class="fa-regular fa-file-lines file-icon-list"></i>
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="fill-${fileId}"></div>
                    </div>
                    <span class="percent" id="perc-${fileId}">0%</span>
                </div>
            </div>
            <i class="fa-solid fa-xmark remove-file" onclick="this.parentElement.remove()"></i>
        `;
        listElement.appendChild(li);

        simulateProgress(fileId);

        if (currentEditingAgentId) {
            const agent = agents.find(a => a.id === currentEditingAgentId);
            if (agent && !agent.arquivos.includes(file.name)) {
                agent.arquivos.push(file.name);
            }
        }
    });

    const inputId = listElement.id === 'fileListAdd' ? 'docsFileAdd' : 'docsFileConfig';
    document.getElementById(inputId).value = "";
}

function simulateProgress(fileId) {
    let progress = 0;
    const fill = document.getElementById(`fill-${fileId}`);
    const perc = document.getElementById(`perc-${fileId}`);

    const interval = setInterval(() => {
        progress += Math.floor(Math.random() * 15) + 5;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }
        if (fill) fill.style.width = progress + '%';
        if (perc) perc.innerText = progress + '%';
    }, 200);
}

document.addEventListener('DOMContentLoaded', () => {

    initUploadBehavior('dropZoneAdd', 'docsFileAdd', 'fileListAdd');
    
    initUploadBehavior('dropZoneConfig', 'docsFileConfig', 'docsListConfig');
});