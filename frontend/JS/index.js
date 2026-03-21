const modal = document.getElementById('modalAgente');
const btnAbrir = document.getElementById('abrirModal');
const btnFechar = document.getElementById('fecharModal');

btnAbrir.onclick = () => {
    modal.showModal();
}

btnFechar.onclick = () => {
    modal.close();
}