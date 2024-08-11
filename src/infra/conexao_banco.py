import sqlite3
import os


class ConexaoBanco:
    conexao = None

    @classmethod
    def conectar_banco(cls):
        caminho_banco = os.path.join(
            os.getcwd(), 'banco', 'web_sraping_produtos.sqlite'
        )
        db_conexao = sqlite3.connect(
            caminho_banco
        )
        cls.conexao = db_conexao
