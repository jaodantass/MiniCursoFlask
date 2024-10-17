// Aguarda até que todo o conteúdo do DOM seja carregado antes de executar o código
document.addEventListener("DOMContentLoaded", function() {
    // Captura o formulário de status (assumindo que é o único formulário na página)
    const statusForm = document.querySelector('form');

    // Adiciona um event listener para o envio do formulário
    statusForm.addEventListener('submit', function(event) {
        // Obtém o valor do campo de status selecionado
        const status = document.getElementById('status').value;

        // Exibe uma caixa de confirmação perguntando ao usuário se ele deseja alterar o status
        const confirmar = confirm(`Tem certeza que deseja alterar o status da tarefa para ${status}?`);

        // Se o usuário clicar em "Cancelar", o envio do formulário é interrompido
        if (!confirmar) {
            event.preventDefault();  // Impede o envio do formulário caso o usuário cancele
        }
    });
});
