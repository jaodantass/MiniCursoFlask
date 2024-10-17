from controle.controlegeral import ControleGeral

class Tarefa(ControleGeral):
    """
    Classe que representa uma Tarefa e herda de ControleGeral para interagir com o banco de dados.
    """

    def __init__(self):
        """
        Construtor da classe Tarefa. Inicializa os atributos da tarefa.
        """
        super().__init__()
        self.__id = ''
        self.__titulo = ''
        self.__descricao = ''
        self.__status = ''
        self.__usuario_id = ''
        self.__criado_em = ''
        self.__atualizado_em = ''

    # Propriedades (getters e setters) para cada atributo da classe

    @property
    def id(self):
        """Retorna o ID da tarefa."""
        return self.__id

    @property
    def titulo(self):
        """Retorna o título da tarefa."""
        return self.__titulo

    @property
    def descricao(self):
        """Retorna a descrição da tarefa."""
        return self.__descricao

    @property
    def status(self):
        """Retorna o status da tarefa (Pendente, Concluída, etc)."""
        return self.__status

    @property
    def usuario_id(self):
        """Retorna o ID do usuário associado à tarefa."""
        return self.__usuario_id

    @property
    def criado_em(self):
        """Retorna a data de criação da tarefa."""
        return self.__criado_em

    @property
    def atualizado_em(self):
        """Retorna a data da última atualização da tarefa."""
        return self.__atualizado_em

    # Setters para modificar os atributos

    @id.setter
    def id(self, entrada):
        """Define o ID da tarefa."""
        self.__id = entrada

    @titulo.setter
    def titulo(self, entrada):
        """Define o título da tarefa."""
        self.__titulo = entrada

    @descricao.setter
    def descricao(self, entrada):
        """Define a descrição da tarefa."""
        self.__descricao = entrada

    @status.setter
    def status(self, entrada):
        """Define o status da tarefa."""
        self.__status = entrada

    @usuario_id.setter
    def usuario_id(self, entrada):
        """Define o ID do usuário associado à tarefa."""
        self.__usuario_id = entrada

    @criado_em.setter
    def criado_em(self, entrada):
        """Define a data de criação da tarefa."""
        self.__criado_em = entrada

    @atualizado_em.setter
    def atualizado_em(self, entrada):
        """Define a data da última atualização da tarefa."""
        self.__atualizado_em = entrada

    # Métodos da classe

    def gettarefa(self):
        """
        Retorna um dicionário com os dados da tarefa.
        """
        dados = {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'status': self.status,
            'usuario_id': self.usuario_id,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }
        return dados

    def settarefa(self, id, titulo, descricao, status, usuario_id, criado_em, atualizado_em):
        """
        Define os atributos da tarefa com base nos valores passados como parâmetros.
        """
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.usuario_id = usuario_id
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def converte(self, a):
        """
        Converte uma tupla de dados em uma tarefa, utilizando settarefa.
        """
        self.settarefa(*a)

    def __eq__(self, entrada):
        """
        Verifica se duas tarefas são iguais, comparando seus atributos.
        """
        retorno = (self.id == entrada.id and
                   self.titulo == entrada.titulo and
                   self.descricao == entrada.descricao and
                   self.status == entrada.status and
                   self.usuario_id == entrada.usuario_id and
                   self.criado_em == entrada.criado_em and
                   self.atualizado_em == entrada.atualizado_em)
        return retorno

    def __str__(self):
        """
        Retorna uma representação em string da tarefa.
        """
        return (f'id={self.__id}, titulo={self.__titulo}, descricao={self.__descricao}, '
                f'status={self.__status}, usuario_id={self.__usuario_id}, '
                f'criado_em={self.__criado_em}, atualizado_em={self.__atualizado_em}')

    # Métodos para interação com o banco de dados

    def incluir(self):
        """
        Insere uma nova tarefa no banco de dados.
        """
        sql = ("INSERT INTO tarefas (titulo, descricao, status, usuario_id) "
               "VALUES ('{}', '{}', '{}', '{}')").format(self.titulo, self.descricao, self.status, self.usuario_id)
        super().incluir(sql)

    def excluir(self):
        """
        Exclui a tarefa do banco de dados com base no ID.
        """
        sql = "DELETE FROM tarefas WHERE id='{}'".format(self.id)
        super().excluir(sql)

    def atualizar(self):
        """
        Atualiza os dados da tarefa no banco de dados com base no ID.
        """
        sql = ("UPDATE tarefas SET titulo='{}', descricao='{}', status='{}', usuario_id='{}', atualizado_em=NOW() "
               "WHERE id='{}'").format(self.titulo, self.descricao, self.status, self.usuario_id, self.id)
        super().alterar(sql)

    def buscar_tarefa_por_id(self, tarefa_id):
        """
        Busca uma tarefa no banco de dados com base no ID.
        """
        sql = "SELECT * FROM tarefas WHERE id='{}'".format(tarefa_id)
        resultado = super().pesquisar(sql)
        if resultado:
            self.converte(resultado)
            return self
        return None

    def listar_tarefas(self):
        """
        Lista todas as tarefas, incluindo o nome do usuário associado.
        """
        sql = """
            SELECT t.id, t.titulo, t.descricao, t.status, t.usuario_id, u.nome_usuario
            FROM tarefas t
            JOIN usuarios u ON t.usuario_id = u.id
        """
        resultados = super().listar_todos(sql)
        tarefas_list = []
        for resultado in resultados:
            nova_tarefa = Tarefa()
            nova_tarefa.id = resultado[0]
            nova_tarefa.titulo = resultado[1]
            nova_tarefa.descricao = resultado[2]
            nova_tarefa.status = resultado[3]
            nova_tarefa.usuario_id = resultado[4]
            nova_tarefa.usuario_nome = resultado[5]  # Adiciona o nome do usuário à tarefa
            tarefas_list.append(nova_tarefa)
        return tarefas_list

    def obter_tarefas_por_usuario(self, usuario_id):
        """
        Obtém todas as tarefas associadas a um usuário específico, utilizando o ID do usuário.
        """
        sql = "SELECT * FROM tarefas WHERE usuario_id='{}'".format(usuario_id)
        resultados = self.listar_todos(sql)
        tarefas = []
        for resultado in resultados:
            tarefa_obj = {
                'id': resultado[0],
                'titulo': resultado[1],
                'descricao': resultado[2],
                'status': resultado[3],
                'usuario_id': resultado[4],
                'criado_em': resultado[5],
                'atualizado_em': resultado[6]
            }
            tarefas.append(tarefa_obj)
        return tarefas
