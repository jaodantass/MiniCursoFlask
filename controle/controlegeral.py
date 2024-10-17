from controle.conectarbanco import Banco
import os
import pymysql


class ControleGeral:
    """
    Classe base que gerencia a interação com o banco de dados.
    Ele utiliza a classe Banco para abrir e fechar conexões, executar consultas e
    gerenciar transações como inclusão, alteração e exclusão de registros.
    """

    def __init__(self):
        """
        Construtor da classe ControleGeral.
        Ele inicializa uma instância da classe Banco e configura os parâmetros de conexão
        com o banco de dados.
        """
        self.ob = Banco()  # Instância da classe Banco
        self.ob.configura(ho="localhost", db="gerenciador_tarefas", us="root",
                          se=os.getenv('DB_PASSWORD'))  # Configura o banco

    def incluir(self, consulta):
        """
        Executa uma operação de inclusão (INSERT) no banco de dados.

        Parâmetros:
        consulta: str - A consulta SQL para a inclusão do registro.
        """
        self.ob.abrirConexao()  # Abre a conexão com o banco
        try:
            self.ob.execute(consulta)  # Executa a consulta SQL
            self.ob.gravar()  # Confirma a transação
            print("\nRegistro inserido com sucesso\n")
        except pymysql.Error as e:
            print(f"Erro no banco de dados: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro no banco de dados
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro inesperado
        finally:
            self.ob.fecharConexao()  # Fecha a conexão com o banco

    def alterar(self, consulta):
        """
        Executa uma operação de alteração (UPDATE) no banco de dados.

        Parâmetros:
        consulta: str - A consulta SQL para alterar o registro.
        """
        self.ob.abrirConexao()  # Abre a conexão com o banco
        try:
            self.ob.execute(consulta)  # Executa a consulta SQL
            self.ob.gravar()  # Confirma a transação
            print("\nRegistro alterado com sucesso\n")
        except pymysql.Error as e:
            print(f"Erro no banco de dados: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro no banco de dados
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro inesperado
        finally:
            self.ob.fecharConexao()  # Fecha a conexão com o banco

    def excluir(self, consulta):
        """
        Executa uma operação de exclusão (DELETE) no banco de dados.

        Parâmetros:
        consulta: str - A consulta SQL para excluir o registro.
        """
        self.ob.abrirConexao()  # Abre a conexão com o banco
        try:
            self.ob.execute(consulta)  # Executa a consulta SQL
            self.ob.gravar()  # Confirma a transação
            print("\nRegistro excluído com sucesso\n")
        except pymysql.Error as e:
            print(f"Erro no banco de dados: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro no banco de dados
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro inesperado
        finally:
            self.ob.fecharConexao()  # Fecha a conexão com o banco

    def pesquisar(self, consulta):
        """
        Executa uma operação de pesquisa (SELECT) no banco de dados.

        Parâmetros:
        consulta: str - A consulta SQL para pesquisar um registro.

        Retorno:
        tuple ou None - O resultado da consulta ou None caso não haja resultado.
        """
        self.ob.abrirConexao()  # Abre a conexão com o banco
        try:
            resultado = self.ob.selectQuery(consulta)  # Executa a consulta SQL
            return resultado[0] if resultado else None  # Retorna o primeiro registro ou None
        except pymysql.Error as e:
            print(f"Erro no banco de dados: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro no banco de dados
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro inesperado
            return None
        finally:
            self.ob.fecharConexao()  # Fecha a conexão com o banco

    def listar_todos(self, consulta):
        """
        Executa uma operação de listagem de todos os registros (SELECT) no banco de dados.

        Parâmetros:
        consulta: str - A consulta SQL para listar todos os registros.

        Retorno:
        list - A lista de todos os resultados ou uma lista vazia em caso de erro.
        """
        self.ob.abrirConexao()  # Abre a conexão com o banco
        try:
            return self.ob.selectQuery(consulta)  # Executa a consulta SQL e retorna todos os resultados
        except pymysql.Error as e:
            print(f"Erro no banco de dados: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro no banco de dados
            return []
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.ob.descarte()  # Desfaz a transação em caso de erro inesperado
            return []
        finally:
            self.ob.fecharConexao()  # Fecha a conexão com o banco
