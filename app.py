from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from modelo.Usuario import Usuario  # Modelo de usuários
from modelo.Tarefa import Tarefa  # Modelo de tarefas
from controle.controlegeral import ControleGeral  # Controle para interagir com o banco de dados
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=30)  # Definindo o tempo de sessão permanente

controle_geral = ControleGeral()

# --------------------------------------------- Rotas de Autenticação ---------------------------------------------

# Rota principal (index) redireciona para login ou dashboard
@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.json.get('nome_usuario')  # Receber os dados como JSON
        senha = request.json.get('senha')

        # Cria uma instância da classe 'usuarios'
        user_instance = Usuario()

        # Autenticar usuário no banco de dados
        user = user_instance.pesquisar_usuario_por_nome(nome_usuario)

        if user and check_password_hash(user['senha_hash'], senha):  # Agora acessamos como dicionário
            session.permanent = True
            session['usuario'] = {'nome': user['nome_usuario'], 'id': user['id'], 'papel': user['papel']}
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'invalido'})

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    # Aqui será feita a lógica de logout, removendo a sessão
    pass


# --------------------------------------------- Dashboard ---------------------------------------------

# Rota do Dashboard
@app.route('/dashboard')
def dashboard():
    # Aqui será exibido o dashboard com base no tipo de usuário
    pass


# --------------------------------------------- Gerenciamento de Tarefas (Admin) ---------------------------------------------

# Rota para Gerenciar Tarefas (Admin)
@app.route('/gerenciar_tarefas', methods=['GET'])
def gerenciar_tarefas():
    # Aqui será exibida a lista de tarefas para o administrador
    pass

# Rota para salvar tarefa (Admin) - criar ou atualizar
@app.route('/salvar_tarefa', methods=['POST'])
def salvar_tarefa():
    # Aqui será salva a tarefa, seja uma criação ou atualização
    pass

# Rota para excluir tarefa (Admin)
@app.route('/excluir_tarefa/<int:id>', methods=['POST'])
def excluir_tarefa(id):
    # Aqui será feita a lógica para excluir uma tarefa
    pass


# --------------------------------------------- Gerenciamento de Usuários (Admin) ---------------------------------------------

# Rota para Gerenciamento de Usuários (Admin)
@app.route('/gerenciar_usuarios', methods=['GET'])
def gerenciar_usuarios():
    # Aqui será exibida a lista de usuários para o administrador
    pass

# Rota para salvar usuário (Admin) - criar ou editar
@app.route('/salvar_usuario', methods=['POST'])
def salvar_usuario():
    # Aqui será salvo o usuário, seja uma criação ou atualização
    pass

# Rota para excluir usuário (Admin)
@app.route('/excluir_usuario/<int:id>', methods=['POST'])
def excluir_usuario(id):
    # Aqui será feita a lógica para excluir um usuário
    pass


# --------------------------------------------- Detalhar Tarefa (Usuário) ---------------------------------------------

# Rota para Detalhar Tarefa (Usuário)
@app.route('/detalhar_tarefa/<int:id>', methods=['GET'])
def detalhar_tarefa(id):
    # Aqui será exibido o detalhe da tarefa para o usuário
    pass

# Rota para Alterar Status da Tarefa (Usuário)
@app.route('/alterar_status_tarefa/<int:id>', methods=['POST'])
def alterar_status_tarefa(id):
    # Aqui será feita a alteração do status da tarefa pelo usuário
    pass


if __name__ == '__main__':
    app.run(debug=True)
