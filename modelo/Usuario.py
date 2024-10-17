from controle.controlegeral import ControleGeral

class Usuario(ControleGeral):
    """
    Classe que representa um Usuário e herda de ControleGeral para interagir com o banco de dados.
    """

    def __init__(self):
        """
        Construtor da classe Usuario. Inicializa os atributos da classe.
        """
        super().__init__()
        self.__id = ''
        self.__nome_usuario = ''
        self.__senha_hash = ''
        self.__papel = ''
        self.__criado_em = ''

    # Propriedades (getters e setters) para acessar e modificar os atributos da classe

    @property
    def id(self):
        """Retorna o ID do usuário."""
        return self.__id

    @property
    def nome_usuario(self):
        """Retorna o nome de usuário."""
        return self.__nome_usuario

    @property
    def senha_hash(self):
        """Retorna o hash da senha do usuário."""
        return self.__senha_hash

    @property
    def papel(self):
        """Retorna o papel do usuário (admin, usuário, etc)."""
        return self.__papel

    @property
    def criado_em(self):
        """Retorna a data de criação do usuário."""
        return self.__criado_em

    # Setters para modificar os atributos

    @id.setter
    def id(self, entrada):
        """Define o ID do usuário."""
        self.__id = entrada

    @nome_usuario.setter
    def nome_usuario(self, entrada):
        """Define o nome de usuário."""
        self.__nome_usuario = entrada

    @senha_hash.setter
    def senha_hash(self, entrada):
        """Define o hash da senha do usuário."""
        self.__senha_hash = entrada

    @papel.setter
    def papel(self, entrada):
        """Define o papel do usuário."""
        self.__papel = entrada

    @criado_em.setter
    def criado_em(self, entrada):
        """Define a data de criação do usuário."""
        self.__criado_em = entrada

    # Métodos da classe

    def getusuarios(self):
        """
        Retorna um dicionário contendo os dados do usuário.
        """
        dados = {
            'id': self.id,
            'nome_usuario': self.nome_usuario,
            'senha_hash': self.senha_hash,
            'papel': self.papel,
            'criado_em': self.criado_em
        }
        return dados

    def setusuarios(self, id, nome_usuario, senha_hash, papel, criado_em):
        """
        Define os atributos do usuário com base nos valores passados como parâmetros.
        """
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha_hash = senha_hash
        self.papel = papel
        self.criado_em = criado_em

    def converte(self, a):
        """
        Converte uma tupla em um objeto da classe Usuario utilizando o método `setusuarios`.
        """
        self.setusuarios(*a)

    def __eq__(self, entrada):
        """
        Compara dois usuários para verificar se são iguais, comparando seus atributos.
        """
        retorno = (self.id == entrada.id and
                   self.nome_usuario == entrada.nome_usuario and
                   self.senha_hash == entrada.senha_hash and
                   self.papel == entrada.papel and
                   self.criado_em == entrada.criado_em)
        return retorno

    def __str__(self):
        """
        Retorna uma representação em string do objeto usuário.
        """
        return f'{self.__id} {self.__nome_usuario} {self.__senha_hash} {self.__papel} {self.__criado_em}'

    # Métodos para interação com o banco de dados

    def incluir(self):
        """
        Insere um novo usuário no banco de dados.
        """
        sql = ("INSERT INTO usuarios (nome_usuario, senha_hash, papel) "
               "VALUES ('{}', '{}', '{}')".format(self.nome_usuario, self.senha_hash, self.papel))
        super().incluir(sql)

    def excluir(self):
        """
        Exclui o usuário do banco de dados com base no ID.
        """
        sql = "DELETE FROM usuarios WHERE id='{}'".format(self.id)
        super().excluir(sql)

    def atualizar(self):
        """
        Atualiza os dados do usuário no banco de dados com base no ID.
        """
        sql = ("UPDATE usuarios SET nome_usuario='{}', senha_hash='{}', papel='{}' WHERE id='{}'"
               ).format(self.nome_usuario, self.senha_hash, self.papel, self.id)
        super().alterar(sql)

    def pesquisar_usuario_por_nome(self, nome_usuario):
        """
        Pesquisa um usuário no banco de dados pelo nome de usuário.
        Retorna os dados do usuário como um dicionário.
        """
        sql = "SELECT * FROM usuarios WHERE nome_usuario='{}'".format(nome_usuario)
        resultado = super().pesquisar(sql)
        if resultado:
            # Cria um dicionário com os dados retornados do banco de dados
            colunas = ['id', 'nome_usuario', 'senha_hash', 'papel', 'criado_em']
            usuario = dict(zip(colunas, resultado))  # Combina colunas com valores do resultado
            return usuario
        return None

    def listaTodos(self):
        """
        Lista todos os usuários do banco de dados.
        Retorna uma lista de objetos da classe Usuario.
        """
        sql = "SELECT * FROM usuarios"
        resultados = super().listar_todos(sql)
        usuarios_list = []
        for resultado in resultados:
            usuario = Usuario()
            usuario.converte(resultado)  # Converte cada resultado em um objeto Usuario
            usuarios_list.append(usuario)
        return usuarios_list
