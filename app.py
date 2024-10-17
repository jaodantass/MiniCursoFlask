from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from modelo.usuario import usuarios  # Modelo de usuários
from modelo.tarefa import tarefa  # Modelo de tarefas
from controle.controlegeral import ControleGeral  # Controle para interagir com o banco de dados
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=30)  # Definindo o tempo de sessão permanente

controle_geral = ControleGeral()


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
        user_instance = usuarios()

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
    session.pop('usuario', None)  # Remove o usuário da sessão
    flash('Você foi desconectado com sucesso!', 'info')
    return redirect(url_for('login'))


# Rota do Dashboard
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Se o usuário for admin, redireciona para o painel de tarefas e usuários
    if session['usuario']['papel'] == 'admin':
        return render_template('dashboard.html')  # Renderiza o dashboard para admins

    # Caso contrário, exibe as tarefas do usuário
    else:
        # Obtenha as tarefas do usuário logado
        usuario_id = session['usuario']['id']
        tarefa_instance = tarefa()  # Criar instância da classe 'tarefa'
        tarefas = tarefa_instance.obter_tarefas_por_usuario(usuario_id)  # Chamar o método corretamente
        return render_template('dashboard.html', tarefas=tarefas)  # Renderiza o dashboard para usuários comuns


# --------------------------------------------- Gerenciamento de Tarefas (Admin) ---------------------------------------------

@app.route('/gerenciar_tarefas', methods=['GET'])
def gerenciar_tarefas():
    if 'usuario' not in session or session['usuario']['papel'] != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))

    # Busca todas as tarefas
    tarefas = tarefa().listar_tarefas()

    # Busca todos os usuários para o dropdown de atribuição de tarefas
    usuarios_list = usuarios().listaTodos()

    return render_template('gerenciar_tarefas.html', tarefas=tarefas, usuarios=usuarios_list)

@app.route('/salvar_tarefa', methods=['POST'])
def salvar_tarefa():
    if 'usuario' not in session or session['usuario']['papel'] != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))

    titulo = request.form['titulo']
    descricao = request.form['descricao']
    status = request.form['status']
    usuario_id = request.form['usuario_id']
    id_tarefa = request.form.get('id')  # Pegue o ID da tarefa, se existir

    # Instância da classe tarefa
    nova_tarefa = tarefa()

    if id_tarefa:  # Se houver um ID, atualize a tarefa existente
        nova_tarefa = nova_tarefa.buscar_tarefa_por_id(id_tarefa)
        if nova_tarefa:
            nova_tarefa.titulo = titulo
            nova_tarefa.descricao = descricao
            nova_tarefa.status = status
            nova_tarefa.usuario_id = usuario_id
            nova_tarefa.atualizar()
            flash('Tarefa atualizada com sucesso!', 'success')
        else:
            flash('Tarefa não encontrada.', 'danger')
    else:  # Senão, crie uma nova tarefa
        nova_tarefa.titulo = titulo
        nova_tarefa.descricao = descricao
        nova_tarefa.status = status
        nova_tarefa.usuario_id = usuario_id
        nova_tarefa.incluir()
        flash('Tarefa criada com sucesso!', 'success')

    return redirect(url_for('gerenciar_tarefas'))

@app.route('/excluir_tarefa/<int:id>', methods=['POST'])
def excluir_tarefa(id):
    if 'usuario' not in session or session['usuario']['papel'] != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))

    # Excluir tarefa
    tarefa_excluir = tarefa()
    tarefa_excluir.id = id
    tarefa_excluir.excluir()

    flash('Tarefa excluída com sucesso.', 'success')
    return redirect(url_for('gerenciar_tarefas'))


# --------------------------------------------- Gerenciamento de Usuários (Admin) ---------------------------------------------

# Rota para Gerenciamento de Usuários (Admin)
@app.route('/gerenciar_usuarios', methods=['GET'])
def gerenciar_usuarios():
    if 'usuario' not in session or session['usuario']['papel'] != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))

    controle = ControleGeral()
    lista_usuarios = usuarios().listaTodos()
    return render_template('gerenciar_usuarios.html', usuarios=lista_usuarios)


# Rota para Adicionar ou Editar Usuário (Admin)
@app.route('/salvar_usuario', methods=['POST'])
def salvar_usuario():
    if 'usuario' not in session or session['usuario']['papel'] != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))

    nome_usuario = request.form['nome_usuario']
    senha = request.form['senha']
    papel = request.form['papel']
    id_usuario = request.form.get('id')

    controle = ControleGeral()
    if id_usuario:  # Se houver um ID, estamos editando
        usuario = usuarios()
        usuario.id = id_usuario
        usuario.nome_usuario = nome_usuario
        usuario.senha_hash = generate_password_hash(senha)
        usuario.papel = papel
        usuario.atualizar()  # Implementar o método `atualizar` no modelo
        flash('Usuário atualizado com sucesso!', 'success')
    else:  # Novo usuário
        usuario = usuarios()
        usuario.nome_usuario = nome_usuario
        usuario.senha_hash = generate_password_hash(senha)
        usuario.papel = papel
        usuario.incluir()
        flash('Usuário adicionado com sucesso!', 'success')

    return redirect(url_for('gerenciar_usuarios'))


# Rota para Excluir Usuário (Admin)
@app.route('/excluir_usuario/<int:id>', methods=['POST'])
def excluir_usuario(id):
    if 'usuario' not in session or session['usuario']['papel'] != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))

    usuario = usuarios()
    usuario.id = id
    print(usuario)
    usuario.excluir()
    flash('Usuário excluído com sucesso!', 'success')

    return redirect(url_for('gerenciar_usuarios'))

# --------------------------------------------- Detalhar Tarefa (Usuário) ---------------------------------------------

# Rota para Detalhar Tarefa (Usuário)
@app.route('/detalhar_tarefa/<int:id>', methods=['GET'])
def detalhar_tarefa(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Buscar a tarefa pelo ID
    tarefa_detalhe = tarefa().buscar_tarefa_por_id(id)

    if tarefa_detalhe is None:
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('detalhar_tarefa.html', tarefa=tarefa_detalhe)


# Rota para Alterar Status da Tarefa (Usuário)
@app.route('/alterar_status_tarefa/<int:id>', methods=['POST'])
def alterar_status_tarefa(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Buscar a tarefa para alteração
    tarefa_status = tarefa().buscar_tarefa_por_id(id)

    if tarefa_status is None:
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('dashboard'))

    # Atualizar o status
    tarefa_status.status = request.form['status']
    tarefa_status.atualizar()

    flash('Status da tarefa atualizado com sucesso.', 'success')
    return redirect(url_for('detalhar_tarefa', id=id))


if __name__ == '__main__':
    app.run(debug=True)