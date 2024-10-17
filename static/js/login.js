// Adiciona um event listener para o formulário de login que escuta o evento 'submit'
document.getElementById("loginForm").addEventListener("submit", function(event) {
    // Impede o comportamento padrão do formulário, que é recarregar a página ao enviar
    event.preventDefault();

    // Obtém os valores inseridos no campo de nome de usuário e senha
    var nome_usuario = document.getElementById("username").value;
    var senha = document.getElementById("senha").value;

    // Faz uma requisição POST para a rota '/login' usando o fetch API
    fetch('/login', {
        method: 'POST',  // Define o método HTTP como POST, usado para enviar dados ao servidor
        headers: {
            'Content-Type': 'application/json'  // Define o tipo de conteúdo como JSON para a requisição
        },
        // Transforma os dados do nome de usuário e senha em uma string JSON e os envia no corpo da requisição
        body: JSON.stringify({ nome_usuario: nome_usuario, senha: senha })
    })
    .then(response => response.json())  // Converte a resposta do servidor para JSON
    .then(data => {
        // Verifica se o status retornado é 'invalido', ou seja, login falhou
        if (data.status === 'invalido') {
            // Exibe um alerta informando que o nome de usuário ou senha estão incorretos
            alert('Nome de usuário ou senha incorretos');
        } else {
            // Se o login for bem-sucedido, redireciona o usuário para o dashboard
            window.location.href = '/dashboard';
        }
    })
    // Em caso de erro durante a requisição, exibe o erro no console
    .catch(error => console.error('Error:', error));
});
