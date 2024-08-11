from typing import Dict
from src.infra.conexao_banco import ConexaoBanco
from src.infra.interface.idatabaserepositorio import IDatabaseRepositorio


class DatabaseRepositorio(IDatabaseRepositorio):
    @classmethod
    def inserir_produtos(self, dados: Dict):
        consulta = """
            INSERT INTO STG_PRODUTOS
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = ConexaoBanco.conexao.cursor()
        cursor.execute(consulta, list(dados.values()))
        ConexaoBanco.conexao.close()
