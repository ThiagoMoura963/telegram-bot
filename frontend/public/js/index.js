let currentEditingAgentId = null;

let agents = [
    { id: 1, nome: "Suporte TI", 
        descricao: "Agente para suporte de TI", 
        instrucao: "Responder tickets de nível 1", 
        token: "123456789:ABCDefghIJKLmnoPQRstuvWXyz-1234567890",
        arquivos: ["manual_ti.pdf"] 
    },
    { id: 2, nome: "Vendas Bot", 
        descricao: "Agente para vendas", 
        instrucao: "Pela imagem, parece que você tentou colocar o botão.", 
        token: "123456789:ABCDefghIJKLmnoPQRstuvWXyz-1234567890",
        arquivos: []
    }
];

function switchTab(tabId, event) {
    const targetEl = event.currentTarget || event;
    const modal = targetEl.closest('dialog');
    
    modal.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    modal.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    
    const btn = modal.querySelector(`button[onclick*="${tabId}"]`);
    if (btn) btn.classList.add('active');
}

function createCardHTML(agent){
    return `
        <div class="agent-card" data-id="${agent.id}">
            <div class="card-header">
                <div class="info">
                    <h3>${agent.nome}</h3>
                </div>
            </div>
            <p class="card-desc">${agent.descricao}</p>
            <div class="card-footer">
                <button class="config-card-btn" onclick="configAgent(${agent.id})">
                    <i class="fa-solid fa-pen"></i> Editar
                </button>
            </div>
        </div>
    `;
}

function closeModal(){
    const buttons = document.querySelectorAll('.cancel-btn, close-x');
    buttons.forEach(btn => {
        btn.onclick = () => {
            const modal = btn.closest('dialog');
            modal.querySelectorAll('input[type="file"]').forEach(input => input.value = "");
            modal.close();
        };
    });
}

function saveAgent(agent){
    const index = agents.findIndex(a => a.id === agent.id);

    agents[index].nome = document.getElementById('nameConfig').value;
    agents[index].descricao = document.getElementById('descriptionConfig').value;
    agents[index].instrucao = document.getElementById('instructionConfig').value;
    agents[index].token = document.getElementById('tokenTelegramConfig').value;
}   

function addAgent(){
    const modal = document.getElementById('modalAgent');
    const form = modal.querySelector('form');

    form.reset();
    document.getElementById('fileListAdd').innerHTML = "";

    modal.showModal();

    switchTab('tab-general-add', modal);

    document.getElementById('saveAdd').onclick = () => {

        const uploadedFiles = [];
        document.querySelectorAll('#fileListAdd .file-name').forEach(el => {
            uploadedFiles.push(el.innerText);
        });
        
        let agent = {
            id: agents.length + 1, 
            nome: document.getElementById('name').value, 
            descricao: document.getElementById('description').value,
            instrucao: document.getElementById('instruction').value, 
            token: document.getElementById('tokenTelegram').value,
            arquivos: uploadedFiles
        };
        
        agents.push(agent);
        renderAgents();
        modal.close();
    }
}

function configAgent(id){
    const agent = agents.find(a => a.id === id);
    const modal = document.getElementById('modalConfig');

    if(agent){
        document.getElementById("nameConfig").value= agent.nome;
        document.getElementById("descriptionConfig").value = agent.descricao;
        document.getElementById("instructionConfig").value = agent.instrucao;
        document.getElementById("tokenTelegramConfig").value = agent.token;

        const listConfig = document.getElementById('docsListConfig');
        listConfig.innerHTML = ""; 

        if(agent.arquivos){
            agent.arquivos.forEach(fileName => {
                const li = document.createElement('li');
                li.className = 'file-item';
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

        switchTab('tab-general-config', modal);

        document.getElementById('saveConfig').onclick = () => {
            saveAgent(agent);
            renderAgents();
            modal.close();
        }
    }
}

function removeFileFromAgent(agentId, fileName, element) {
    const agent = agents.find(a => a.id === agentId);
    if(agent) {
        agent.arquivos = agent.arquivos.filter(f => f !== fileName);
        element.parentElement.remove();
    }
}

function renderAgents(){
    const grid = document.querySelector('#gridAgents');
    grid.innerHTML = "";

    agents.forEach(agent => {
        const card = createCardHTML(agent);
        grid.insertAdjacentHTML('beforeend', card);
    });
}

renderAgents();
closeModal();

