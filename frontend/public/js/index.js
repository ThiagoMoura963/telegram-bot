let agents = [
    { id: 1, nome: "Suporte TI", descricao: "Agente para suporte de TI", instrucao: "Responder tickets de nível 1", token: "123456789:ABCDefghIJKLmnoPQRstuvWXyz-1234567890" },
    { id: 2, nome: "Vendas Bot", descricao: "Agente para vendas", instrucao: "Pela imagem, parece que você tentou colocar o botão de criação dentro da Navbar ou usou Flexbox sem definir o espaço corretamente. O ideal é que o botão de criação fique abaixo da Navbar e centralizado na página, conforme o layout de dashboard que geramos.", token: "123456789:ABCDefghIJKLmnoPQRstuvWXyz-1234567890" }
];

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
                    <i class="fa-solid fa-gear"></i> Configurar
                </button>
            </div>
        </div>
    `;
}

function closeModal(){
    const buttons = document.querySelectorAll('.cancel-btn');
    buttons.forEach(btn => {
        btn.onclick = () => {
            btn.closest('dialog').close();
        };
    });
}

function saveAgent(agent){
    const index = agents.findIndex(a => a.id === agent.id);

    agents[index].nome = document.getElementById('nameConfig').value;
    agents[index].instrucao = document.getElementById('instructionConfig').value;
    agents[index].token = document.getElementById('tokenTelegramConfig').value;
}   

function addAgent(){
    const modal = document.getElementById('modalAgent');

    modal.showModal();

    document.getElementById('saveAdd').onclick = () => {
        let agent = {
            id: agents.length + 1, 
            nome: document.getElementById('name').value, 
            descricao: document.getElementById('description'),
            instrucao: document.getElementById('instruction').value, 
            token: document.getElementById('tokenTelegram').value
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
        document.getElementById("nameConfig").setAttribute("value", agent.nome);
        document.getElementById("descriptionConfig").value = agent.descricao;
        document.getElementById("instructionConfig").value = agent.instrucao;
        document.getElementById("tokenTelegramConfig").value = agent.token;

        modal.showModal();

        document.getElementById('saveConfig').onclick = () => {
            saveAgent(agent);
            renderAgents();
            modal.close();
        }
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

