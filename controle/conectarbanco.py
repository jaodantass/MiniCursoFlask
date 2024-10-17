import os
import pymysql


class Banco:
    """
    Classe responsável por gerenciar a conexão e a interação com o banco de dados MySQL.
    """

    def __init__(self):
        """
        Construtor da classe Banco. Inicializa as variáveis de conexão com o banco de dados.
        """
        self.servidor = "localhost"  # Host do banco de dados (normalmente 'localhost' ou IP do servidor)
        self.usuario = "root"  # Usuário do banco de dados
        self.senha = os.getenv(
            'DB_PASSWORD')  # Pega a senha do banco de dados a partir da variável de ambiente 'DB_PASSWORD'
        self.banco = "gerenciador_tarefas"  # Nome do banco de dados que será acessado
        self.ponteiro = ""  # Ponteiro/cursor para interagir com o banco de dados
        self.con = None  # Inicializa a conexão como None (a conexão será estabelecida no método abrirConexao)

    def abrirConexao(self):
        """
        Abre a conexão com o banco de dados.
        """
        self.con = pymysql.connect(host=self.servidor, db=self.banco, user=self.usuario, passwd=self.senha)
        self.ponteiro = self.con.cursor()  # Cria o cursor para executar queries

    def fecharConexao(self):
        """
        Fecha a conexão com o banco de dados, se ela estiver aberta.
        """
        if self.con:
            self.con.close()  # Fecha a conexão com o banco de dados

    def selectQuery(self, entrada):
        """
        Executa uma consulta (SELECT) no banco de dados e retorna os resultados.

        Parâmetros:
        entrada: str - A query SQL a ser executada.

        Retorno:
        tuple - Os resultados da consulta.
        """
        self.ponteiro.execute(entrada)  # Executa a query SQL
        resposta = self.ponteiro.fetchall()  # Retorna todos os resultados da consulta
        return resposta

    def executeQuery(self, entrada, dados):
        """
        Executa uma query SQL (com dados) no banco de dados.

        Parâmetros:
        entrada: str - A query SQL com placeholders (%s) para os dados.
        dados: tuple - Os dados a serem inseridos na query.
        """
        self.ponteiro.execute(entrada, dados)  # Executa a query com os dados passados

    def execute(self, entrada):
        """
        Executa uma query SQL sem dados adicionais (normalmente usada para queries simples, como DELETE ou UPDATE).

        Parâmetros:
        entrada: str - A query SQL a ser executada.
        """
        self.ponteiro.execute(entrada)  # Executa a query

    def gravar(self):
        """
        Confirma (commita) as mudanças no banco de dados.
        """
        self.con.commit()  # Confirma todas as operações pendentes no banco de dados

    def descarte(self):
        """
        Desfaz (rollback) todas as mudanças não confirmadas no banco de dados.
        """
        self.con.rollback()  # Desfaz todas as operações não confirmadas no banco de dados

    def configura(self, ho, db, se='senha', us='root'):
        """
        Configura as credenciais de conexão com o banco de dados.

        Parâmetros:
        ho: str - O endereço do servidor do banco de dados.
        db: str - O nome do banco de dados.
        se: str - A senha do banco de dados (opcional, padrão 'senha').
        us: str - O nome de usuário do banco de dados (opcional, padrão 'root').
        """
        self.servidor = ho
        self.usuario = us
        self.senha = se
        self.banco = db

    def mostraResultado(self, entrada):
        """
        Exibe os resultados de uma consulta de forma legível no console.

        Parâmetros:
        entrada: tuple - A resposta da consulta a ser mostrada.
        """
        for i in entrada:
            print(i)  # Exibe cada linha do resultado da consulta
