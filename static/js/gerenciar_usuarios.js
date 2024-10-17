// Adiciona um event listener ao documento que será executado assim que o conteúdo DOM for completamente carregado
document.addEventListener("DOMContentLoaded", function() {
    // Obtém o formulário de adição/edição de usuários
    const form = document.getElementById('adicionarUsuarioForm');
    
    // Obtém o botão que alterna a exibição do formulário
    const toggleFormBtn = document.getElementById('toggleFormBtn');
    
    // Obtém a div que contém o formulário
    const formUsuario = document.getElementById('formUsuario');

    // Validação do formulário quando o mesmo for enviado
    form.addEventListener('submit', function(event) {
        // Previne o envio automático do formulário, que recarregaria a página
        event.preventDefault();

        // Captura os valores inseridos nos campos de nome de usuário, senha e papel
        const nomeUsuario = document.getElementById('nome_usuario').value.trim();
        const senha = document.getElementById('senha').value.trim();
        const papel = document.getElementById('papel').value;

        // Valida se o campo nome de usuário não está vazio
        if (nomeUsuario === '') {
            alert('Nome de usuário é obrigatório.');
            return;
        }

        // Valida se a senha tem pelo menos 6 caracteres
        if (senha.length < 6) {
            alert('A senha deve ter pelo menos 6 caracteres.');
            return;
        }

        // Valida se o papel selecionado é um valor permitido ('usuario' ou 'admin')
        if (papel !== 'usuario' && papel !== 'admin') {
            alert('Selecione um papel válido.');
            return;
        }

        // Se todas as validações passarem, o formulário é enviado
        form.submit();
    });

    // Exibe ou oculta o formulário de adição/edição de usuários e limpa os campos quando necessário
    toggleFormBtn.addEventListener('click', function() {
        if (formUsuario.style.display === 'none') {
            // Exibe o formulário e altera o texto do botão para 'Cancelar'
            formUsuario.style.display = 'block';
            toggleFormBtn.textContent = 'Cancelar';
        } else {
            // Oculta o formulário e altera o texto do botão para 'Adicionar Novo Usuário'
            formUsuario.style.display = 'none';
            toggleFormBtn.textContent = 'Adicionar Novo Usuário';
            // Limpa os campos do formulário quando cancelado
            limparCamposFormulario();
        }
    });

    // Função para limpar os campos do formulário
    function limparCamposFormulario() {
        // Limpa os valores dos campos de id, nome de usuário e senha
        document.getElementById('id').value = '';
        document.getElementById('nome_usuario').value = '';
        document.getElementById('senha').value = '';
        // Redefine o valor do papel para o padrão 'usuario'
        document.getElementById('papel').value = 'usuario';  
    }
});

// Função para editar um usuário, chamada quando o botão de editar é clicado
function editarUsuario(id, nome_usuario, papel) {
    // Preenche os campos do formulário com os dados do usuário selecionado
    document.getElementById('id').value = id;
    document.getElementById('nome_usuario').value = nome_usuario;
    document.getElementById('papel').value = papel;
    document.getElementById('senha').value = '';  // Limpa o campo de senha para forçar o preenchimento de uma nova

    // Exibe o formulário para edição e altera o texto do botão para 'Cancelar'
    document.getElementById('formUsuario').style.display = 'block';
    document.getElementById('toggleFormBtn').textContent = 'Cancelar';
}
