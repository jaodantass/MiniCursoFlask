// Adiciona um event listener para garantir que o código só seja executado após o conteúdo do DOM ser completamente carregado
document.addEventListener("DOMContentLoaded", function() {
    // Captura os elementos do formulário e botões
    const form = document.getElementById('adicionarTarefaForm');
    const toggleFormBtn = document.getElementById('toggleFormBtn');
    const formTarefa = document.getElementById('formTarefa');
    const idField = document.getElementById('id');  // Campo hidden que armazena o ID da tarefa (para edição)

    // Adiciona um event listener ao formulário para validar e controlar seu envio
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Previne o comportamento padrão do envio do formulário

        // Captura os valores dos campos do formulário
        const titulo = document.getElementById('titulo').value.trim();
        const descricao = document.getElementById('descricao').value.trim();
        const status = document.getElementById('status').value;
        const usuario_id = document.getElementById('usuario_id').value;
        const id = idField.value;  // Verifica se existe um ID (indica que é uma edição)

        // Validações simples do formulário
        if (titulo === '') {
            alert('Título é obrigatório.');  // O título da tarefa não pode estar vazio
            return;
        }

        if (descricao.length < 10) {
            alert('A descrição deve ter pelo menos 10 caracteres.');  // A descrição precisa ter um mínimo de 10 caracteres
            return;
        }

        if (usuario_id === '') {
            alert('Selecione um usuário.');  // O campo de usuário não pode estar vazio
            return;
        }

        // Verifica se estamos criando uma nova tarefa ou editando uma existente
        if (id) {
            form.action = `/salvar_tarefa`;  // Define a ação do formulário para salvar a tarefa editada
        } else {
            form.action = `/salvar_tarefa`;  // Define a ação do formulário para criar uma nova tarefa
        }

        // Submete o formulário após as validações
        form.submit();
    });

    // Controle da exibição do formulário para adicionar/editar uma tarefa
    toggleFormBtn.addEventListener('click', function() {
        if (formTarefa.style.display === 'none') {
            // Se o formulário estiver oculto, exibe e altera o texto do botão para 'Cancelar'
            formTarefa.style.display = 'block';
            toggleFormBtn.textContent = 'Cancelar';
        } else {
            // Se o formulário estiver visível, oculta e altera o texto do botão para 'Adicionar Nova Tarefa'
            formTarefa.style.display = 'none';
            toggleFormBtn.textContent = 'Adicionar Nova Tarefa';
            limparFormulario();  // Limpa os campos do formulário
        }
    });
});

// Função para limpar os campos do formulário ao adicionar nova tarefa
function limparFormulario() {
    document.getElementById('id').value = '';  // Limpa o ID (indica que é uma nova tarefa)
    document.getElementById('titulo').value = '';  // Limpa o campo de título
    document.getElementById('descricao').value = '';  // Limpa o campo de descrição
    document.getElementById('status').value = 'Pendente';  // Define o status padrão como 'Pendente'
    document.getElementById('usuario_id').value = '';  // Limpa o campo de seleção de usuário
}

// Função para carregar os dados de uma tarefa no formulário para edição
function editarTarefa(id, titulo, descricao, status, usuario_id) {
    // Preenche os campos do formulário com os dados da tarefa a ser editada
    document.getElementById('id').value = id;  // Preenche o ID da tarefa
    document.getElementById('titulo').value = titulo;  // Preenche o título da tarefa
    document.getElementById('descricao').value = descricao;  // Preenche a descrição da tarefa
    document.getElementById('status').value = status;  // Preenche o status da tarefa
    document.getElementById('usuario_id').value = usuario_id;  // Preenche o usuário associado à tarefa

    // Exibe o formulário para edição
    document.getElementById('formTarefa').style.display = 'block';
    document.getElementById('toggleFormBtn').textContent = 'Cancelar';  // Altera o texto do botão para 'Cancelar'
}
