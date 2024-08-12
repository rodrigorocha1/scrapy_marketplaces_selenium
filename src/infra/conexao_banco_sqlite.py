import sqlite3
import os
from typing import Dict
from src.infra.interface.iconexaodatabase import IconexaoDatabase


class ConexaoBancoSQLITE(IconexaoDatabase):
    def __init__(self) -> None:
        self.__caminho_banco = os.path.join(
            os.getcwd(), 'banco', 'web_sraping_produtos.sqlite'
        )
        self.__conexao = None
        self.__cursor = None

    def conectar_banco(self):
        self.__conexao = sqlite3.connect(self.__caminho_banco)
        self.__cursor = self.__conexao.cursor()

    def desconectar_banco(self):
        if self.__conexao:
            self.__cursor.close()
            self.__conexao.close()

    def inserir_produtos(self, dados: Dict):
        if not self.__conexao or not self.__cursor:
            self.conectar_banco()

        consulta = """
            INSERT INTO STG_PRODUTOS
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.__cursor.execute(consulta, list(dados.values()))
        self.__conexao.commit()

    def __del__(self):
        self.desconectar_banco()
